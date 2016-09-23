import cherrypy
import time
import socket

class ToxicPlayerCommunicator():

    connected_to_timbl = False

    chat_sockets = {}
    ports = {'toxic': 7078, 'normal': 7079}

    def predict(self,text):

        if not self.connected_to_timbl:
            self.connect_to_timbl()

        toxic_answer = self.send_to_timbl('toxic',text)
        normal_answer = self.send_to_timbl('normal',text)

        return toxic_answer+'\t'+normal_answer

    def connect_to_timbl(self, host='', retry=20, interval=1):
        """ Connect to a Timbl server"""

        for socket_label in ['toxic','normal']:

            self.chat_sockets[socket_label] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.chat_sockets[socket_label].settimeout(120)

            while retry > 0:
                retry -= 1

                try:
                    self.chat_sockets[socket_label].connect((host, int(self.ports[socket_label])))
                    self.chat_sockets[socket_label].recv(1024)  # Ignore welcome messages
                except socket.error:
                    time.sleep(interval)
                    continue

                self.connected_to_timbl = True
                break

        return self.connected_to_timbl

    def send_to_timbl(self, socket_label, words_to_classify):

        #Sending
        number_of_words = len(words_to_classify.split())
        while number_of_words < 20:
            words_to_classify += ' _'
            number_of_words+= 1

        message = 'c '+words_to_classify+' ?\n'
        self.chat_sockets[socket_label].sendall(message.encode())

        time.sleep(0.5)

        #Receiving
        receiving_content = True
        buffer = b''
        while receiving_content:
            chunk = self.chat_sockets[socket_label].recv(1024)
            if not chunk or str(chunk[-1]) == '\n': #newline
                receiving_content = False
            buffer += chunk

        return buffer.decode()[10:-2]

if __name__ == '__main__':

    c = ToxicPlayerCommunicator()

    while True:
        print(c.predict(raw_input()))