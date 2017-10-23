import sys
import os
import json
from item import *
from ItemManager import *

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
