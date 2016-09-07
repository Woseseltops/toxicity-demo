import os

class Instance():
    def __init__(self, features, classname):
        self.features = features
        self.classname = classname

    def get_timbl_str(self):
        return ' '.join(self.features + [self.classname])


def add_items_to_list_until_length(l, item, length):
    while len(l) < length:
        l.append(item)

    return l

def import_lol_data_file(input_path,maximum_message_length):

    toxic_instances = []
    normal_instances = []

    previous_chat_message = None
    previous_author = None
    instance = None

    for line in open(input_path):

        #Info about speaker signals a chat message
        if '[ally]' in line or '[reported]' in line or '[enemy]' in line:

            author, time, chat_message, linebreak = line.split('\t')

            #We're only interested in replies
            if previous_chat_message != None:

                #Add it to the previous instance if the author was the same
                if author == previous_author:

                    if instance != None:
                        instance.classname+= '_/_'+chat_message.replace(' ','_')

                #This is a new instance
                else:
                    features = add_items_to_list_until_length(previous_chat_message.split(), '_',
                                                              maximum_message_length)[:maximum_message_length]
                    classname = chat_message.replace(' ', '_')
                    instance = Instance(features, classname)

                    if '[reported]' in author:
                        toxic_instances.append(instance)
                    else:
                        normal_instances.append(instance)

            previous_chat_message = chat_message
            previous_author = author

        #Info about the game signals a new game
        elif 'Game type' in line:
            previous_chat_message = None

    return normal_instances, toxic_instances

def export_to_timbl_format():

    pass

if __name__ == '__main__':
    INPUT_PATH = '/vol/bigdata2/datasets2/LoL/ExtractedData/'
    OUTPUT_FOLDER = '/home/wstoop/toxicity-demo/data/'

    MAXIMUM_CHAT_LENGTH = 20

    normal_instance_file = open(OUTPUT_FOLDER+'normal_chat.inst','w')
    toxic_instance_file = open(OUTPUT_FOLDER+'toxic_chat.inst','w')

    nr_of_files = len(os.listdir(INPUT_PATH))

    for n,filename in enumerate(os.listdir(INPUT_PATH)):

        if n%100 == 0:
            print(n/nr_of_files,'%')

        normal_instances, toxic_instances = import_lol_data_file(INPUT_PATH+filename,MAXIMUM_CHAT_LENGTH)

        for instance in normal_instances:
            normal_instance_file.write(instance.get_timbl_str()+'\n')

        for instance in toxic_instances:
            toxic_instance_file.write(instance.get_timbl_str()+'\n')

#TODO
# Skip long sentences
# glue meerdere dingen together