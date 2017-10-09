from tkinter import *
from tkinter import ttk

def main():
    root = Tk()
    root.title("Grocery List Manager")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    listbox = Listbox(root)
    listbox.insert(END,item)

if __name__ == '__main__':
    main()
