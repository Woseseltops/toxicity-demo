from copy import copy

class Instance():

    def __init__(self,features,classname):
        
        self.features = features
        self.classname = classname

    def get_timbl_str(self):
        return ' '.join(self.features+[self.classname])

def add_items_to_list_until_length(l,item,length):
    
    while len(l) < length:
        l.append(item)

    return l

if __name__ == '__main__':
    INPUT_FILE = '/home/wstoop/toxicity-demo/data/example.txt'

    split_messages = [message.split() for message in open(INPUT_FILE)]
    longest_message = max([len(message) for message in split_messages])

    last_message = ['_']
    instances = []
    for n, words in enumerate(reversed(split_messages)):
        features = add_items_to_list_until_length(copy(words),'_',longest_message)
        classname = '_'.join(last_message)
        instances.append(Instance(features,classname))
        last_message = words

    for instance in instances:
        print(instance.get_timbl_str())
