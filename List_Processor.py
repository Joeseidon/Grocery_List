from item import *
import re
import json
import datetime
import time
import os

class ListProcessor:
    old_list_read = False
    new_list_read = False

    def __init__(self, target_list="GroceryList.txt",commone_items_obj="Common_items.json"):
        self.CURRENT_LIST = target_list
        self.NEEDED_ITEMS_JSON = commone_items_obj
        self.List_Date = ''
        self.Current_Date = datetime.datetime.today().strftime('%m/%d/%y')
        self.current_list = []
        self.needed_items = []
        self.items_to_remove = []
        self.past_items = []

    def process_list(self,debug=False):
        try:
            self.generate_past_list(debugging=debug)
            self.generate_current_list(debugging=debug)
            self.item_list_to_file(self.determine_needed_items(debugging = debug))
            #Rewrite Common Items reference file
            self.rewrite_Common_Items_File()
        except:
            return False
        return True
    def getCurrentList(self):
        return current_list
    def determine_needed_items(self,debugging = False):
        #Used to convert fractions from textfile to a usable formatter_class
        _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t,str) else t

        #Analyize date
        #Determine if the list is out of date and indicate that in the txt file
        #if out of date recommendations don't change in this script
        if(self.old_list_read == True  and self.new_list_read == True):
            if(not len(self.past_items) == 0):
                #perform action
                found = False
                count = 1
                for item in self.past_items:
                    for i in self.current_list:
                        if debugging:
                            print(str(count)+"::"+"comparing: " + str(item) +" and "+str(i))
                        count+=1
                        try:
                            if item.get_name() in i.get_name():
                                found = True
                                break
                        except:
                            if item.get_name() in _u(i.get_name()):
                                found = True
                                break
                    if debugging:
                        print("######Found(False = Needed Item)########")
                        print(found)
                    if not found:
                        item.increment_weeks_past()
                        if(item.needed()):
                            if debugging:
                                print("needed: "+item.get_name())
                            self.needed_items.append(item)
                            item.reset_weeks_past()
                    else:
                        item.increment_weeks_past()
                        if not(item.needed()):
                            self.items_to_remove.append(item)
                        else:
                            item.reset_weeks_past()
                        found = False
                if debugging:
                    print("###############################after########################")
                    self.print_items(self.needed_items)
            return self.needed_items

    def generate_past_list(self,debugging = False):
        with open(self.NEEDED_ITEMS_JSON, 'r') as f:
            data = json.load(f)

        for i in data["PastItems"]:
            r = item(name=i["name"],quantity=i["quantity"],
                        frequency=i["frequency"],wW=i["weeksWithout"],
                        units_cont = i["unitType"])
            self.past_items.append(r)

        if debugging:
            print("###############################Past#################################")
            self.print_items(self.past_items)
        self.old_list_read = True

    def generate_current_list(self,debugging = False):
        bullet_list = False
        file = open(self.CURRENT_LIST,"r")
        for line in file:
            if("Grocery List for Performance Software to be delivered" in line):
                match = re.search('\d{2}/\d{2}/\d{2}',line)
                self.List_Date = match.group(0)
            if ((not("Grocery List for Performance Software to be delivered" in line))
                    and not (line in ['\n', '\r\n', ' '])
                    and not("----------------------" in line)
                    and not line == None):
                if("Everything below the line will not be ordered (for copy & paste - previous weeks)" in line):
                    break
                quantity = ""
                index = 0
                for char in line:
                    if char.isdigit():
                        index += 1
                        quantity += char
                    else:
                        break
                strItem = re.search('.+\S',line)
                if not (strItem == None):
                    i = item(name=strItem.group(0)[index:],quantity=quantity)
                    self.current_list.append(i)

        file.close()
        if debugging:
            print("###############################Current List#################################")
            self.print_items(self.current_list)
        self.new_list_read = True

    def clear_file(self,filename):
        file = open(filename,"w")
        file.truncate(0)

    def print_items(self,listp):
        for item in listp:
            print(item)

    def list_out_of_date(self):
        list_d = time.strptime(self.List_Date, "%m/%d/%y")
        current_d = time.strptime(self.Current_Date, "%m/%d/%y")
        if(current_d > list_d):
            return True
        else:
            return False

    def item_list_to_file(self,itemlist,filename="neededItems.txt"):
        file = open(filename, "w")
        if self.list_out_of_date():
            file.write("The current list is out of date as of "
                        +self.Current_Date+
                        ".\nThe following recommendations are based on what is currently in the list.\n")
        else:
            file.write("These recommendations are for the delivery for the week of: "+self.List_Date+"\n")
        for i in itemlist:
            file.write(i.toString()+"\n")
        if self.items_to_remove:
            file.write("\nThe following items appear to be unneeded for this next week based on past habits: \n")
            for item in self.items_to_remove:
                file.write(item.toString()+"\n")
        file.close()

    def update_Weeks_Past(self,p_itemlist):
        for p_item in p_itemlist:
            p_item.increment_weeks_past()

    def rewrite_Common_Items_File(self):
        #update json structure for item changes made during processing
        newListJson = []
        for i in self.past_items:
            newListJson.append(
                {"weeksWithout": i.get_weeks_past(),
                 "frequency"   : i.get_frequency(),
            	 "quantity"    : i.get_quantity(),
            	 "name"        : i.get_name(),
                 "unitType"    : i.get_unitType()
            })
        newDic = {"PastItems":newListJson}
        with open(self.NEEDED_ITEMS_JSON, 'w') as f:
            json.dump(newDic, f)

if __name__ == '__main__':
    L = ListProcessor()
    L.process_list(debug=True)
