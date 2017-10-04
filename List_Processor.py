from item import *

class ListProcessor:
    NEEDED_ITEMS_FILE = "Common_Items.txt"
    CURRENT_LIST = "current_list.txt"

    def __init__(self):
        self.current_list = []

        self.past_items = []

    def generate_past_list(self,debugging = False):
        file = open(self.NEEDED_ITEMS_FILE,"r")
        i = 0
        for line in file:
            elements = line.split(",")
            for e in elements:
                desc = e.split(":")
                r = item(desc[0],desc[1],desc[2])
                self.past_items.append(r)
        file.close()
        if debugging:
            print"###############################Past#################################"
            print self.past_items

    def generate_current_list(self,debugging = False):
        file = open(self.CURRENT_LIST,"r")
        i = 0
        for line in file:
            elements = line.split(",")
            for e in elements:
                desc = e.split(":")
                if(len(desc)>1):
                    r = item(desc[1],desc[0])
                else:
                    r = item(desc[0])
                self.current_list.append(r)
        file.close()
        if debugging:
            print"###############################Current#################################"
            print self.current_list

    def clear_file(self,filename):
        file = open(filename,"w")
        file.truncate(0)

if __name__ == '__main__':
    listp = ListProcessor()
    listp.generate_past_list(True)
    listp.generate_current_list(True)
