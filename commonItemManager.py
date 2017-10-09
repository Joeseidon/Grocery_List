import sys
import os
import json

def main():
    choice_execution = {1:getFileName,2:listItems,3:removeItem,4:addItem,5:list_json_files,6:exit}
    while True:
        mainMenu = """\tChoose File      ->  1
                    \n\tList Items       ->  2
                    \n\tRemove Item      ->  3
                    \n\tEnter Item       ->  4
                    \n\tList JSON Files  ->  5
                    \n\tExit Program     ->  6"""
        print("Main Menu:\n"+mainMenu)
        try:
            choice = int(raw_input("What are you here to do?: "))
            while not (choice > 0 and choice < 7):
                choice = int(raw_input("Please choose a valid option: "))
            if(choice>1 and choice<5):
                choice_execution[choice](filename)
            elif(choice==1):
                filename = choice_execution[choice]()
            else:
                choice_execution[choice]()
        except:
            print("Error: Invalid Entry\n\n")

def list_json_files():
    cur_dir = os.getcwd()
    file_list = os.listdir(cur_dir)
    for file in file_list:
        name = file.split('.')
        if(name[1] == 'json'):
            print(file)

def addItem(filename):
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
    itemData["quantity"]=answer
    valid = False

    while not valid:
        answer = raw_input("Frequency (integer): ")
        if answer.isdigit():
            valid = True

    itemData["frequency"]=answer
    valid = False

    with open(filename,'r+') as f:
        try:
            data = json.load(f)
            f.seek(0)
            data["PastItems"].append(itemData)
            json.dump(data,f)
        except:
            newlist=[itemData]
            json.dump({"PastItems":newlist},f)
def listItems(filename):
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
            if data:
                for i in data["PastItems"]:
                    item_desc = """\n%s\n\tUnits: %s\n\tQuantity: %s\n\tFrequency: %s\n\tWeeks Without: %s""" %(i["name"],i["unitType"], i["quantity"], i["frequency"],i["weeksWithout"])
                    print(item_desc)
        except:
            print("No JSON structure detected.")
    f.close()

def removeItem(filename):
    answer = raw_input("Enter name of item to be removed: ")
    with open(filename, 'r+') as f:
        try:
            data = json.load(f)
            #newList = []
            for item in data["PastItems"]:
                #print(item["name"]+'vs'+answer)
                if (item["name"] == answer):
                    #newList.append(item)
                    del data["PastItems"][data["PastItems"].index(item)]
            #newDic = {"PastItems":newList}
            f.seek(0)
            #json.dump(newDic,f)
            json.dump(data,f)
            f.close()
        except:
            print("No original data found.\n\n")

def exit():
    sys.exit()

def getFileName():
    fileFound = False
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        while not fileExists(filename):
            failmsg = """The file you provided, %s, was not found.""" %(filename)
            filename=fileprompt(msg=failmsg)
    else:
        filename = fileprompt()
        while not fileExists(filename):
            failmsg = """The file you provided, %s, was not found.""" %(filename)
            fileprompt(msg=failmsg)

    return filename

def fileprompt(msg=None):
    if msg:
        print(msg)
    filename = raw_input("Please enter a JSON filename: ")
    return filename

def fileExists(filename):
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
                return True
            if answer in valid_n:
                return False

if __name__ == '__main__':
    main()
