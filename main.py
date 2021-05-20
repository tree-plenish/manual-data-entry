import _tkinter
import tkinter as tk
from tkinter import ttk

from customWidgets import AutocompleteDropdown

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Tree Plenish Manual Data Entry")
        self.master.geometry("500x300")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.leftFrame = tk.Frame(self.master)
        self.leftFrame.pack(side=tk.LEFT, anchor=tk.NE)
        
        self.rightFrame = tk.Frame(self.master)
        self.rightFrame.pack(side=tk.RIGHT, anchor=tk.NW)

        self.bottomFrame = tk.Frame(self.master)
        self.bottomFrame.pack(side=tk.BOTTOM)
        
        self.label = tk.Label(self, text = "Tree Plenish Manual Data Entry")
        self.label.pack()

        self.typeLabel = tk.Label(self.leftFrame, text = "Select Data Entry Type" )
        self.typeLabel.pack(padx = 3, pady = 3)
        self.typeDropdown = ttk.Combobox(self.rightFrame, state = "readonly", values = ["Add", "Delete", "Modify"])
        self.typeDropdown.pack(padx = 3, pady = 3)
        
        self.entryPtLabel = tk.Label(self.leftFrame, text = "Select Entry Point" )
        self.entryPtLabel.pack(padx = 3, pady = 3)
        self.entryPtDropdown = ttk.Combobox(self.rightFrame, state = "readonly", values = ["Typeform", "Other"])
        self.entryPtDropdown.pack(padx = 3, pady = 3)

        self.entryPtDropdown.bind("<<ComboboxSelected>>", self.setAdditionalOptions)

        # self.submitButton = tk.Button(self.bottomFrame, text = "Submit", command = self.retrieveData)
        # self.submitButton.pack(padx = 3, pady = 3)

    def retrieveData(self):
        print("Type: ", self.typeDropdown.get())
        print("Entry Point: ", self.entryPtDropdown.get())

    def setAdditionalOptions(self, event):
        if self.entryPtDropdown.get() == "Typeform":
            self.formIDLabel = tk.Label(self.leftFrame, text = "Enter Typeform ID" )
            self.formIDLabel.pack(padx = 3, pady = 3)
            self.formIDEntry = tk.Entry(self.rightFrame, width = 20)
            self.formIDEntry.insert(0,"Example: ")
            self.formIDEntry.pack(padx = 5, pady = 5)

            self.stage = 0
            self.nextButton = tk.Button(self.bottomFrame, text = "Next", command = self.next)
            self.nextButton.pack(side = tk.LEFT, padx = 3, pady = 3)
        else:
            try:
                self.formIDLabel.destroy()
                self.formIDEntry.destroy()
                self.scrollbar.destroy()
                self.lb.destroy()
                self.listFrame.destroy()
                self.searchBox.destroy()
                self.getFormButton.destroy()
            except:
                pass
    
    def getForm(self):
        formID = self.formIDEntry.get()
        self.questions = ['C','C++','Java', 'Python','Perl',
                               'PHP','ASP','JS', 'test2', 'test3', 
                            'test1', 'test4', 'test5', 'test6' ] # get list of questions from formID
        self.searchBox = AutocompleteDropdown(self.leftFrame, choices=self.questions)
        self.searchBox.pack()

    def next(self):
        if self.stage == 0: # submit question id; get specific typeform questions and ask specific form info
            self.getForm()
        elif self.stage == 1: # submit specific form submission; ask what field to change
            return
        self.stage += 1


root = tk.Tk()
app = Application(master=root)
app.mainloop() # Triggers GUI
