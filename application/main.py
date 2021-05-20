import _tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


from customWidgets import AutocompleteDropdown, WrapLabel

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Tree Plenish Manual Data Entry")
        self.master.geometry("500x500")
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

        self.emailLabel = tk.Label(self.leftFrame, text = "Enter your email" )
        self.emailLabel.pack(padx = 3, pady = 3)
        self.emailEntry = tk.Entry(self.rightFrame)
        # self.emailEntry.insert(0,"Example: ")
        self.emailEntry.pack(padx = 5, pady = 5)


        self.typeLabel = tk.Label(self.leftFrame, text = "Select Data Entry Type" )
        self.typeLabel.pack(padx = 3, pady = 3)
        self.typeDropdown = ttk.Combobox(self.rightFrame, state = "readonly", values = ["Add", "Delete", "Modify"])
        self.typeDropdown.pack(padx = 3, pady = 3)
        
        self.entryPtLabel = tk.Label(self.leftFrame, text = "Select Entry Point" )
        self.entryPtLabel.pack(padx = 3, pady = 3)
        self.entryPtDropdown = ttk.Combobox(self.rightFrame, state = "readonly", values = ["Typeform", "Other"])
        self.entryPtDropdown.pack(padx = 3, pady = 3)

        self.entryPtDropdown.bind("<<ComboboxSelected>>", self.setAdditionalOptions)

        self.stage = -1
        self.nextFunc = [self.askForFormID, self.askForSubmissionQ, self.askForSubmissionA, self.askForChangeQ, self.askForChangeA]
        # self.submitButton = tk.Button(self.bottomFrame, text = "Submit", command = self.retrieveData)
        # self.submitButton.pack(padx = 3, pady = 3)

    def retrieveData(self):
        print("Type: ", self.typeDropdown.get())
        print("Entry Point: ", self.entryPtDropdown.get())

    def setAdditionalOptions(self, event):
        if self.entryPtDropdown.get() == "Typeform":
            if self.stage == -1:
                self.prevButton = tk.Button(self.bottomFrame, text = "Back", command = self.prevStage)
                self.prevButton.pack(side = tk.LEFT, padx = 3, pady = 3)
                self.nextButton = tk.Button(self.bottomFrame, text = "Next", command = self.nextStage)
                self.nextButton.pack(side = tk.RIGHT, padx = 3, pady = 3)
            else:
                self.stage = -1

            # initialize typeform related widgets
            self.stageText = WrapLabel(self.leftFrame, text="")
            self.formIDBox = AutocompleteDropdown(self.rightFrame, choices=[])
            self.submissionQBox = AutocompleteDropdown(self.rightFrame, choices=[])
            self.submissionABox = AutocompleteDropdown(self.rightFrame, choices=[])
            self.changeQBox = AutocompleteDropdown(self.rightFrame, choices=[])
            self.changeABox = tk.Entry(self.rightFrame, width = 20)
            self.fields = [self.formIDBox, self.submissionQBox, self.submissionABox, self.changeQBox, self.changeABox]
            self.nextStage()


        else:
            # come back to this later
            # try:
            #     self.formIDLabel.destroy()
            #     self.formIDEntry.destroy()
            #     self.scrollbar.destroy()
            #     self.lb.destroy()
            #     self.listFrame.destroy()
            #     self.searchBox.destroy()
            #     self.getFormButton.destroy()
            # except:
            #     pass
            return

    def nextStage(self):
        if self.stage < len(self.nextFunc)-1:
            if isinstance(self.fields[self.stage], AutocompleteDropdown):
                if not self.fields[self.stage].verify():
                    # pop up error
                    tk.messagebox.showerror("Error", "Please select one of the options listed.")
                    return
            self.stage += 1
            self.nextFunc[self.stage]()
        self.fields[self.stage].config(state="normal")
        if self.stage > 0:
            self.fields[self.stage-1].config(state="disabled")


    def prevStage(self):
        if self.stage > 0:
            if isinstance(self.fields[self.stage], AutocompleteDropdown):
                if not self.fields[self.stage].verify():
                    # pop up error
                    messagebox.showerror("Error", "Please select one of the options listed.")
                    return
            self.stage -= 1
            self.nextFunc[self.stage]()
        self.fields[self.stage].config(state="normal")
        if self.stage < len(self.nextFunc)-1:
            self.fields[self.stage+1].config(state="disabled")

    def askForFormID(self):
        self.stageText.config(text="Enter Typeform ID")
        self.stageText.pack(padx = 3, pady = 3)

        formIDs = ['1','2','3','4','5','6','4574','2124' ] # get list of form IDs
        self.formIDBox.config(choices=formIDs)
        self.formIDBox.pack(padx = 5, pady = 5)

    def askForSubmissionQ(self):
        formID = self.formIDBox.get()        

        self.questions = ['C','C++','Java', 'Python','Perl',
                               'PHP','JS','test2', 'test3', 
                            'test1', 'test4', 'test5', 'test6' ] # get list of questions from formID
        self.submissionQBox.config(choices=self.questions)
        self.submissionQBox.pack(padx = 5, pady = 5)
        self.stageText.config(text="Edit the specific form submission with the following question-response pair. Select the question:")

        
    def askForSubmissionA(self):
        question = self.submissionQBox.get()
        # get responses to chosen question...
        responses = ['a', 'b', 'c']
                
        self.submissionABox.config(choices=responses)
        self.submissionABox.pack(padx = 5, pady = 5)
        
        self.stageText.config(text="Edit the specific form submission with the following question-response pair. Select the response:")

    def askForChangeQ(self):
        answer = self.submissionABox.get()
        # get specific submission based on question and answer
        # ask user to choose question of the answer field they want to change
        
        self.changeQBox.config(choices=self.questions)
        self.changeQBox.pack(padx = 5, pady = 5)
        self.stageText.config(text="Choose question field to change")

    def askForChangeA(self):
        question = self.changeQBox.get()
        # get current answer to display
                
        self.changeABox.insert(0,"Current response")
        self.changeABox.pack(padx = 5, pady = 5)
        self.stageText.config(text="Change response to:")

    # To do: use API, confirmation, submit and save data to json


root = tk.Tk()
app = Application(master=root)
app.mainloop() # Triggers GUI
