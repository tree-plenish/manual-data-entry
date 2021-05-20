import _tkinter
import tkinter as tk
from tkinter import ttk

from customWidgets import AutocompleteDropdown, WrapLabel

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Tree Plenish Manual Data Entry")
        self.master.geometry("500x300")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.mainContent = tk.Frame(self.master)
        self.mainContent.pack()
        self.mainContent.grid_columnconfigure(0, weight=1, uniform="group1")
        self.mainContent.grid_columnconfigure(1, weight=1, uniform="group1")
        self.mainContent.grid_rowconfigure(0, weight=1)

        self.leftFrame = tk.Frame(self.mainContent)
        # self.leftFrame.pack(side=tk.LEFT, anchor=tk.NE)
        self.rightFrame = tk.Frame(self.mainContent)
        # self.rightFrame.pack(side=tk.RIGHT, anchor=tk.NW)

        self.leftFrame.grid(row=0, column=0, sticky="nsew")
        self.rightFrame.grid(row=0, column=1, sticky="nsew")

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

        self.stage = 0
        self.nextFunc = [self.askForSubmission, self.askForSubmissionChange]
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

            if self.stage == 0:
                self.nextButton = tk.Button(self.bottomFrame, text = "Next", command = self.nextStage)
                self.nextButton.pack(side = tk.LEFT, padx = 3, pady = 3)
            else:
                self.stage = 0
        else:
            # come back to this later
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

    def nextStage(self):
        if self.stage < len(self.nextFunc):
            self.nextFunc[self.stage]()
            self.stage += 1
    
    def askForSubmission(self):
        formID = self.formIDEntry.get()

        self.stageText = WrapLabel(self.leftFrame, 
                                    text="Edit the specific form submission with the following question-response pair. Select the question:")
        self.stageText.pack(padx = 3, pady = 3)

        questions = ['C','C++','Java', 'Python','Perl',
                               'PHP','JS','test2', 'test3', 
                            'test1', 'test4', 'test5', 'test6' ] # get list of questions from formID
        self.searchBox = AutocompleteDropdown(self.rightFrame, choices=questions)
        self.searchBox.pack(padx = 5, pady = 5)
        
    def askForSubmissionChange(self):
        question = self.searchBox.get()
        # get responses to chosen question...
        responses = ['a', 'b', 'c']
        self.searchBox.config(choices=responses)
        self.stageText.config(text="Edit the specific form submission with the following question-response pair. Select the response:")

root = tk.Tk()
app = Application(master=root)
app.mainloop() # Triggers GUI
