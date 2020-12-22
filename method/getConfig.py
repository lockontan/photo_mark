import configparser
import os

path = os.path.join(os.getcwd(), 'config.ini')

class getConfig():

    def __init__(self):
        cf = configparser.ConfigParser()
        if not os.path.exists(path):
            f = open(path,"w")
            f.close()
            cf.read(path)

            cf.add_section('homeData')
            cf.set('homeData', 'workpath', '')
            cf.set('homeData', 'mark', '')
            cf.add_section('sendData')
            cf.set('sendData', 'outbox', '')

            with open(path,"w") as f:
                cf.write(f)
        cf.read(path)
        self.cf = cf

    def getValue(self, sections, item):
       return self.cf.get(sections, item)
    
    def setValue(self, sections, item, value):
        self.cf.set(sections, item, value)
        self.cf.write(open(path,"w"))