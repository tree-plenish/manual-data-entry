import _tkinter
import tkinter as tk
from tkinter import ttk

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

        self.submitButton = tk.Button(self.bottomFrame, text = "Submit", command = self.retrieveData)
        self.submitButton.pack(padx = 3, pady = 3)

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
            self.getFormButton = tk.Button(self.rightFrame, text = "Go", command = self.getForm)
            self.getFormButton.pack(padx = 3, pady = 3)
        else:
            try:
                self.formIDLabel.destroy()
                self.formIDEntry.destroy()
            except:
                pass
    
    def getForm(self):
        formID = self.formIDEntry.get()
        self.questions = ['C','C++','Java', 'Python','Perl',
                            'PHP','ASP','JS', 'test2', 'test3', 
                            'test1', 'test4', 'test5', 'test6' ] # get list of questions from formID
        #creating text box 
        self.searchBox = tk.Entry(self.leftFrame)
        self.searchBox.pack()
        self.searchBox.bind('<KeyRelease>', self.checkkey)
        # to do: hide/show list box like combobox
        self.searchBox.bind('<ButtonPress-1>', self.toggleList)
        
        #creating list box
        self.listFrame = tk.Frame(self.leftFrame)
        self.listFrame.pack(fill = tk.BOTH)
        self.lb = tk.Listbox(self.listFrame)
        self.lb.pack(side = tk.LEFT, fill = tk.BOTH)
        self.lb.bind("<<ListboxSelect>>", self.updateQuestionSelected)
        self.scrollbar = tk.Scrollbar(self.listFrame)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.lb.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.lb.yview)

        self.updateListbox(self.questions)

    def checkkey(self, event):
        value = self.searchBox.get()
        if value == '':
            data = self.questions
        else:
            data = []
            for item in self.questions:
                if value.lower() in item.lower():
                    data.append(item)
        # update data in listbox
        self.updateListbox(data)
   
    def toggleList(self, event):
        print(event)
   
    def updateListbox(self, data):
        # clear previous data
        self.lb.delete(0, 'end')
        # put new data
        for item in data:
            self.lb.insert('end', item)
    
    def updateQuestionSelected(self, event):
        selection = self.lb.curselection()
        if selection:
            self.searchBox.delete(0,tk.END)
            self.searchBox.insert(0,self.lb.get(selection))
        self.checkkey(None)


root = tk.Tk()
app = Application(master=root)
app.mainloop() # Triggers GUI
