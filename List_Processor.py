from item import *

class ListProcessor:
    NEEDED_ITEMS_FILE = "Common_Items.txt"
    CURRENT_LIST = "GroceryList.txt"
    old_list_read = False
    new_list_read = False

    def __init__(self):
        self.current_list = []
        self.needed_items = []
        self.past_items = []

    def listProcessing(self):
        self.generate_past_list()
        self.generate_current_list()
        self.item_list_to_file(self.determine_needed_items())

    def determine_needed_items(self,debugging = False):
        if(self.old_list_read == True  and self.new_list_read == True):
            if(not len(self.past_items) == 0):
                #perform action
                found = False
                count = 1
                for item in self.past_items:
                    for i in self.current_list:
                        if debugging:
                            print str(count)+"::"+"comparing: " + str(item) +" and "+str(i)
                        count+=1
                        if item.get_name() in i.get_name():
                            found = True
                            break
                    if debugging:
                        print("######Result########")
                        print found
                    if not found:
                        self.needed_items.append(item)
                    else:
                        found = False
                if debugging:
                    print"###############################after########################"
                    self.print_items(self.needed_items)
            return self.needed_items

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
            self.print_items(self.past_items)
        self.old_list_read = True

    def generate_current_list(self,debugging = False):
        file = open(self.CURRENT_LIST,"r")
        for line in file:
            if ((not("Grocery List for Performance Software to be delivered" in line))
                and not (line in ['\n', '\r\n', ' '])
                and not("----------------------" in line)):
                if("Everything below the line will not be ordered (for copy & paste - previous weeks)" in line):
                    break
                #Create new item
                #i = item()
                #Get item name and quantity
                quantity = ""
                index = 0
                for char in line:
                    if char.isdigit():
                        index += 1
                        quantity += char
                    else:
                        break
                i = item(name=line[index:],quantity=quantity)
                self.current_list.append(i)

        file.close()
        if debugging:
            print"###############################Current#################################"
            self.print_items(self.current_list)
            print self.current_list
        self.new_list_read = True

    def clear_file(self,filename):
        file = open(filename,"w")
        file.truncate(0)

    def print_items(self,listp):
        for item in listp:
            print item
    def item_list_to_file(self,itemlist,filename="neededItems.txt"):
        file = open(filename, "w")
        for i in itemlist:
            file.write(i.toString())
        file.close()


if __name__ == '__main__':
    listp = ListProcessor()
    listp.listProcessing()
