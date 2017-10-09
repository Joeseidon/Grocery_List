import sys
import os
import json

def main():
    #Get the file to be edited (must be a json file)
    filename = getFileName()
    choice_execution = {1:addItem,2:listItems,3:removeItem,4:exit}
    while True:
        mainMenu = """\tEnter Item    ->  1
                    \n\tList Items    ->  2
                    \n\tRemove Item   ->  3
                    \n\tExit Program  ->  4"""
        print("\n\nMain Menu:\n"+mainMenu)
        choice = int(raw_input("What are you here to do?: "))
        while not (choice > 0 and choice < 5):
            choice = int(raw_input("Please choose a valid option: "))
        choice_execution[choice](filename)

def addItem(filename):
    return None
def listItems(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    for i in data["PastItems"]:
        item_desc = """\n%s\n\tUnits:%s\n\tQuantity%s\n\tFrequency:%s\n\tWeeks Without:%s""" %(i["name"],i["unitType"], i["quantity"], i["frequency"],i["weeksWithout"])
        print(item_desc)
def removeItem(filename):
    return None
def exit(filename):
    sys.exit()

def getFileName():
    fileFound = False
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if (not(fileExists(filename))):
            while fileFound:
                failmsg = """The file you provided, %s,
                    was not found.""" %(filename)
                filename=fileprompt(msg=failmsg)
    else:
        filename = fileprompt()
        while not fileExists(filename):
            failmsg = """The file you provided, %s,
                was not found.""" %(filename)
            fileprompt(msg=failmsg)

    return filename

def fileprompt(msg=None):
    if msg:
        print(msg)
    filename = raw_input("Please enter a JSON filename: ")
    return filename

def fileExists(filename):
    #take off file extension (.pdf ..etc)
    #strlst = filename.split('.')
    #name = strlst[0]
    cur_dir = os.getcwd()

    file_list = os.listdir(cur_dir)
    if filename in file_list:
        return True
    else:
        #print files for now to debug if there are issues
        for f in file_list:
            print(f)
        return False

if __name__ == '__main__':
    main()
