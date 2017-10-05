from item import *

class ListProcessor:
    NEEDED_ITEMS_FILE = "Common_Items.txt"
    CURRENT_LIST = "current_list.txt"
    old_list_read = False
    new_list_read = False

    def __init__(self):
        self.current_list = []

        self.past_items = []

    def add_needed_items(self,debugging = False):
        if(self.old_list_read == True  and self.new_list_read == True):
            if debugging:
                print"###############################before########################"
                self.print_items(self.current_list)
            if(not len(self.past_items) == 0):
                #perform action
                found = False
                count = 1
                for item in self.past_items:
                    for i in self.current_list:
                        print str(count)+"::"+"comparing: " + str(item) +" and "+str(i)
                        count+=1
                        if i == item:
                            found = True
                            break
                    if debugging:
                        print("######Result########")
                        print found
                    if not found:
                        self.current_list.append(item)
                    else:
                        found = False
                if debugging:
                    print"###############################after########################"
                    self.print_items(self.current_list)

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
        self.old_list_read = True

    def generate_current_list(self,debugging = False):
        file = open(self.CURRENT_LIST,"r")
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
        self.new_list_read = True

    def clear_file(self,filename):
        file = open(filename,"w")
        file.truncate(0)

    def print_items(self,listp):
        for item in listp:
            print item

if __name__ == '__main__':
    listp = ListProcessor()
    listp.generate_past_list(debugging=True)
    listp.generate_current_list(debugging=True)
    listp.add_needed_items(debugging=False)
