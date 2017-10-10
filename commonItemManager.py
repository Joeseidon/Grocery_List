import sys
import os
import json
from item import *

class ItemManager:
    dataloaded = False
    target_file = ""
    currentItemList = []
    newFile = False
    datacreated = False

    def __init__(self):
        pass

    def initialize_file(self,filename):
        self.target_file = filename
        rtn = self.JSONdata_to_itemlist()
        if rtn == None:
            dataload = False
        else:
            dataload = True

    def list_json_files(self):
        print("\nJSON Files in the Current Directory:")
        cur_dir = os.getcwd()
        file_list = os.listdir(cur_dir)
        for file in file_list:
            name = file.split('.')
            if(name[1] == 'json'):
                print("\t"+file)
        print("\n")
    def JSONdata_to_itemlist(self):
        try:
            with open(self.target_file,'r') as f:
                data = json.load(f)
                if data:
                    for i in data["PastItems"]:
                        r = item(name=i["name"],quantity=i["quantity"],
                                    frequency=i["frequency"],wW=i["weeksWithout"],
                                    units_cont = i["unitType"])
                        self.currentItemList.append(r)
                        self.dataloaded = True
        except:
            print("No JSON data found.")

    def itemlist_to_JSONdatafile(self):
        newListJson = []
        if self.dataloaded or self.datacreated:
            for i in self.currentItemList:
                newListJson.append(
                    {"weeksWithout": i.get_weeks_past(),
                     "frequency"   : i.get_frequency(),
                     "quantity"    : i.get_quantity(),
                     "name"        : i.get_name(),
                     "unitType"    : i.get_unitType()
                })
            newDic = {"PastItems":newListJson}
            with open(self.target_file, 'w') as f:
                json.dump(newDic, f)

    def listItems(self):
        if self.dataloaded or self.datacreated:
            print("\nCurrent List: ")
            for item in self.currentItemList:
                print("\t"+item.toString()+"\n")
        else:
            print("Data not found.")

    def dataLoaded(self):
        return self.dataloaded

    def getTargetFile(self):
        return self.target_file

    def continueEditing(self, adding = False, removing = False):
        if not adding and not removing:
            return False
        if adding:
            msg="Add Item: (y/n) "
        if removing:
            msg="Remove Item: (y/n)"

        answer = raw_input(msg)

        valid_y = ["y","Y"]
        valid_n = ["n","N"]
        if answer in valid_y:
            self.addItems() if adding else self.removeItem()
            return True
        if answer in valid_n:
            self.itemlist_to_JSONdatafile()
            return False

    def addItems(self):
        if not self.dataloaded:
            self.datacreated = True
        itemData = {"weeksWithout": 0, "frequency": 0,"quantity" : 0,"name" : "", "unitType": ""}
        print("New Item Data:")
        valid = False

        while not valid:
            answer = raw_input("Name: ")
            if answer and not answer == " ":
                valid = True
        itemData["name"]=answer
        valid = False

        while not valid:
            answer = raw_input("Unit Type: ")
            if answer and not answer == " ":
                valid = True
        itemData["unitType"]=answer
        valid = False

        while not valid:
            answer = raw_input("Quantity (integer): ")
            if answer.isdigit():
                valid = True
        itemData["quantity"] = int(answer)
        valid = False

        while not valid:
            answer = raw_input("Frequency (integer): ")
            if answer.isdigit():
                valid = True

        itemData["frequency"] = int(answer)
        valid = False

        r = item(name=itemData["name"],quantity=itemData["quantity"],
                    frequency=itemData["frequency"],wW=itemData["weeksWithout"],
                    units_cont = itemData["unitType"])
        self.currentItemList.append(r)
        print("\nAdded Item: "+r.toString()+"\n")

    def removeItem(self):
        answer = raw_input("Enter name of item to be removed: ")

        if self.dataloaded or self.datacreated:
            for item in self.currentItemList:
                if item.get_name() == answer:
                    del self.currentItemList[self.currentItemList.index(item)]
        else:
            print("Data not loaded.")

    def getFileName(self):
        self.resetClassVars()
        fileFound = False
        if len(sys.argv) > 1:
            filename = sys.argv[1]
            while not self.fileExists(filename):
                failmsg = """The file you provided, %s, was not found.""" %(filename)
                filename=self.fileprompt(msg=failmsg)
        else:
            filename = self.fileprompt()
            while not self.fileExists(filename):
                failmsg = """The file you provided, %s, was not found.""" %(filename)
                self.fileprompt(msg=failmsg)

        return filename

    def resetClassVars(self):
        self.target_file = ""
        self.newFile = False
        self.dataloaded = False

    def fileprompt(self,msg=None):
        if msg:
            print(msg)
        filename = raw_input("Please enter a JSON filename: ")
        return filename

    def fileExists(self,filename):
        cur_dir = os.getcwd()

        file_list = os.listdir(cur_dir)
        if filename in file_list:
            name = filename.split('.')
            if(name[1] == 'json'):
                return True
            else:
                print("Not of file type .json")
                return False
        else:
            while True:
                answer = raw_input("Provided File doesn't exist. Create new file? (y/n)")
                valid_y = ["y","Y"]
                valid_n = ["n","N"]
                if answer in valid_y:
                    #Create new file
                    f = open(filename,"w")
                    f.close()
                    self.newFile = True
                    return True
                if answer in valid_n:
                    return False

def main():
    manager = ItemManager()
    if(len(sys.argv) == 1):
        #No file specified. Default to common_items.json used by the rest of the script
        manager.initialize_file("Common_items.json")

    while True:
        mainMenu = """\n\tList Items       ->  1
                    \n\tAdd Items        ->  2
                    \n\tRemove Items     ->  3
                    \n\tSwitch File      ->  4
                    \n\tList JSON Files  ->  5
                    \n\tExit Program     ->  6\n"""
        print("Main Menu: (Target file = %s)\n%s"%(manager.getTargetFile(),mainMenu))
        invalid = True
        while invalid:
            try:
                choice = int(raw_input("What are you here to do?: "))
                invalid = False
            except:
                valid = True
        while not (choice > 0 and choice < 7):
            choice = int(raw_input("Please choose a valid option: "))
        if(choice == 4):
            target_file = manager.getFileName()
            manager.initialize_file(target_file)
            if manager.dataLoaded():
                print("Failed to load JSON data.")
        elif(choice == 5):
            manager.list_json_files()
        elif(choice == 1):
            manager.listItems()
        elif(choice == 2):
            while manager.continueEditing(adding = True):
                pass
        elif(choice == 3):
            while manager.continueEditing(removing = True):
                pass
        elif(choice == 6):
            sys.exit(0)

if __name__ == '__main__':
    main()
