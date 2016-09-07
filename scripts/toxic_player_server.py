import cherrypy
import time
import socket

class ToxicPlayerServer(object):

    connected_to_timbl = False
    timblsocket = None

    def predict(self,text):

        if not self.connected_to_timbl:
            self.connect_to_timbl()

        answer = self.send_to_timbl(text)
        return answer

    predict.exposed = True

    def connect_to_timbl(self, port=7078, host='', retry=20, interval=1):
        """ Connect to a Timbl server"""

        self.timblsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while retry > 0:
            retry -= 1

            try:
                self.timblsocket.connect((host, int(port)))
                self.timblsocket.recv(1024)  # Ignore welcome messages
            except socket.error:
                time.sleep(interval)
                continue

            self.connected_to_timbl = True
            break

        return self.connected_to_timbl

    def send_to_timbl(self, words_to_classify):

        number_of_words = len(words_to_classify.split())
        while number_of_words < 20:
            words_to_classify += ' _'
            number_of_words+= 1

        message = 'c '+words_to_classify+' ?\n'

        print(message)

        self.timblsocket.sendall(message.encode())
        return self.timblsocket.recv(1024).decode()[10:-2]

cherrypy.config.update({'server.socket_port': 7077})
cherrypy.quickstart(ToxicPlayerServer())