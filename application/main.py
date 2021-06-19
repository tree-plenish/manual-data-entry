# NOTE: FTP functions are commented out for just application logic without spamming server. 
# Typeform functions are commented out (using dummy data instead) to test GUI while 
# Typeform error is being resolved.
import _tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

from Typeform import Typeform
from customWidgets import AutocompleteDropdown, WrapLabel
# from SendFTP import HandleFTP

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Tree Plenish Manual Data Entry")
        self.master.geometry("500x500")
        self.pack()
        self.create_widgets()
        self.nextFunc = [self.askForFormID, self.askForSubmissionQ, self.askForSubmissionA, self.askForChangeQ, self.askForChangeA, self.submit]

        # Setting class variables for request md and data
        self.md = {}
        self.data = {}

    def create_widgets(self):
        ## Scrollbar for window stuff starts here: 
        ## will make it easier to view multiple modification requests, 
        ## turns out to be more tedius than expected since tkinter scrollbar 
        ## can't directly be attached to a frame (need to use Canvas)

        # scrollable canvas and scrollbar
        self.scrollable = tk.Canvas(self.master, highlightthickness=0)
        self.scrollable.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.scrollable.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure scrollable canvas
        self.scrollable.configure(yscrollcommand=self.scrollbar.set)

        self.innerFrame = tk.Frame(self.scrollable)
        self.scrollable.height = self.scrollable.winfo_reqheight()
        self.scrollable.width = self.scrollable.winfo_reqwidth()
        self.scrollable.create_window((0,0), window=self.innerFrame, anchor="nw", width=self.scrollable.width)
        self.scrollable.addtag_all("resize")
        # allow mousewheel to scroll
        self.scrollable.bind_all("<MouseWheel>", lambda e: self.scrollable.yview_scroll(-1 * int((e.delta / 120)), "units"))
        

        # resize content window width in canvas when window is resized
        # also attach scroll region to scroll bar
        def resizeAndSetScroll(e):
            self.scrollable.scale("resize",0,0,float(e.width)/self.scrollable.width,float(e.height)/self.scrollable.height)
            self.scrollable.width = e.width
            self.scrollable.height = e.height
            self.scrollable.configure(scrollregion=self.scrollable.bbox("all"))
        
        self.scrollable.bind("<Configure>", resizeAndSetScroll)
        self.innerFrame.bind("<Configure>", lambda e: self.scrollable.configure(scrollregion=self.scrollable.bbox("all")))

        ## End scrollbar for window

        self.label = tk.Label(self.innerFrame, text = "Tree Plenish Manual Data Entry")
        self.label.pack()

        self.mainContent = tk.Frame(self.innerFrame)
        self.mainContent.pack()
        self.mainContent.grid_columnconfigure(0, weight=1, uniform="group1")
        self.mainContent.grid_columnconfigure(1, weight=2, uniform="group1")
        self.mainContent.grid_rowconfigure(0, weight=1)

        self.leftFrame = tk.Frame(self.mainContent)
        self.rightFrame = tk.Frame(self.mainContent)

        self.leftFrame.grid(row=0, column=0, sticky="nsew")
        self.rightFrame.grid(row=0, column=1, sticky="nsew")

        self.bottomFrame = tk.Frame(self.innerFrame)
        self.bottomFrame.pack(side=tk.BOTTOM)

        self.emailLabel = tk.Label(self.leftFrame, text = "Enter your email" )
        self.emailLabel.pack(padx = 3, pady = 3)
        self.emailEntry = tk.Entry(self.rightFrame, width=300)
        # self.emailEntry.insert(0,"Example: ")
        self.emailEntry.pack(padx = 20, pady = 5)


        self.typeLabel = tk.Label(self.leftFrame, text = "Select Data Entry Type" )
        self.typeLabel.pack(padx = 3, pady = 3)
        self.typeDropdown = ttk.Combobox(self.rightFrame, state = "readonly", values = ["Add", "Delete", "Modify"])
        self.typeDropdown.pack(padx = 20, pady = 3, fill="both", expand=True)
        
        self.entryPtLabel = tk.Label(self.leftFrame, text = "Select Entry Point" )
        self.entryPtLabel.pack(padx = 3, pady = 3)
        self.entryPtDropdown = ttk.Combobox(self.rightFrame, state = "readonly", values = ["Typeform", "Other"])
        self.entryPtDropdown.pack(padx = 20, pady = 3, fill="both", expand=True)

        self.advance = tk.Button(self.bottomFrame, text = "Next", command = self.setAdditionalOptions)
        self.advance.pack(padx = 3, pady = 3)
        # self.entryPtDropdown.bind("<<ComboboxSelected>>", self.setAdditionalOptions)

        self.stage = -1
        self.reqWidgets = []
        # self.submitButton = tk.Button(self.bottomFrame, text = "Submit", command = self.retrieveData)
        # self.submitButton.pack(padx = 3, pady = 3)        

    def setAdditionalOptions(self):
        # for some reason this loading label is not packed until after the typeform loading delay
        # loadingLabel = WrapLabel(self.innerFrame, text = "Loading..." )
        # loadingLabel.pack(padx = 3, pady = 3)
        # print("loading typeform")

        if self.entryPtDropdown.get() == "" or self.emailEntry.get() == "" or self.typeDropdown.get() == "":
            messagebox.showerror("Error", "Please fill in all required fields")
            return

        # very basic email syntax validation
        regex = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex, self.emailEntry.get()):
            messagebox.showerror("Error", "Please enter a valid email")
            return
 

        self.data["email"] = self.emailEntry.get()
        self.data["type"] = self.typeDropdown.get()
        self.data["entry_point"] = self.entryPtDropdown.get()

        if self.data["entry_point"] == "Typeform" and self.data["type"] == "Modify":
            self.advance.destroy()

            self.requestNum = 0
            self.data["requests"] = [] # array of changes the user wants to make to a form

            self.entryPtDropdown.config(state="disabled")
            self.emailEntry.config(state="disabled")
            self.typeDropdown.config(state="disabled")

            self.typeform = Typeform()

            resetButton = tk.Button(self.bottomFrame, text = "Reset All Fields", command = self.resetWithConfirmation, bg='#cccccc')
            resetButton.pack(side = tk.LEFT, padx = 3, pady = 3)
            self.prevButton = tk.Button(self.bottomFrame, text = "Back", command = self.prevStage)
            self.prevButton.pack(side = tk.LEFT, padx = 3, pady = 3)
            self.nextButton = tk.Button(self.bottomFrame, text = "Next", command = self.nextStage)
            self.nextButton.pack(side = tk.RIGHT, padx = 3, pady = 3)
            self.submitButton = tk.Button(self.bottomFrame, text = "Submit", command = self.submit)
            
            
            # load all forms once here (takes a while, and likely will not change if user clicks back button or requests multiple changes)
            self.forms = []
            # result = self.typeform.get_all_forms()
            result = [{"title":"form1", "id":"1"},{"title":"form2", "id":"2"},{"title":"form3", "id":"3"}]
            for form in result:
                self.forms.append(form["title"] + ", " + form["id"])
            # loadingLabel.pack_forget()

            self.initializeFields()
            
            self.nextStage()

        else:
            # come back to this later...if we want to add other functionalities.
            messagebox.showerror("Error", "This application currently only supports Typeform submission modifications")
            return
    def initializeFields(self):
        divider = ttk.Separator(self.innerFrame,orient='horizontal')
        divider.pack(fill='x', pady=8)

        container = tk.Frame(self.innerFrame)
        container.pack(fill='x')
        container.grid_columnconfigure(0, weight=1, uniform="group1")
        container.grid_columnconfigure(1, weight=2, uniform="group1")
        container.grid_rowconfigure(0, weight=1)

        leftFrame = tk.Frame(container)
        rightFrame = tk.Frame(container)

        leftFrame.grid(row=0, column=0, sticky="nsew")
        rightFrame.grid(row=0, column=1, sticky="nsew")

        #currently for typeform changes only
        formIDBox = AutocompleteDropdown(rightFrame,width = 50, choices=[])
        formIDBox.config(choices=self.forms)
        submissionQBox = AutocompleteDropdown(rightFrame, width = 50, choices=[])
        submissionABox = AutocompleteDropdown(rightFrame, width = 50, choices=[])
        changeQBox = AutocompleteDropdown(rightFrame, width = 50, choices=[])
        changeABox = tk.Entry(rightFrame, width = 50)

        stageText = WrapLabel(leftFrame, text="")
        deleteButton = tk.Button(leftFrame, text = "Delete", bg='#cccccc')
        deleteButton.index = self.requestNum
        deleteButton.config(command = lambda: self.deleteRequest(deleteButton.index)) 
        deleteButton.pack(side = tk.TOP, padx = 3, pady = 3)

        # list of widgets specific to each additional change request
        self.reqWidgets.append([formIDBox, submissionQBox, submissionABox, changeQBox, changeABox, # fields
                                stageText, deleteButton, divider, # other GUI widgets
                                leftFrame, rightFrame, container]) # layout

    def nextStage(self):
        if self.stage < len(self.nextFunc)-1:
            if isinstance(self.reqWidgets[self.requestNum][self.stage], AutocompleteDropdown):
                if not self.reqWidgets[self.requestNum][self.stage].verify():
                    # pop up error
                    messagebox.showerror("Error", "Please select one of the options listed.")
                    return
            self.stage += 1
            self.nextFunc[self.stage]()
        self.reqWidgets[self.requestNum][self.stage].config(state="normal")
        if self.stage > 0:
            self.reqWidgets[self.requestNum][self.stage-1].config(state="disabled")


    def prevStage(self):
        if self.stage > 0:
            self.stage -= 1
            self.nextFunc[self.stage]()
        self.reqWidgets[self.requestNum][self.stage].config(state="normal")
        if self.stage < len(self.nextFunc)-1:
            self.reqWidgets[self.requestNum][self.stage+1].config(state="disabled")

    def askForFormID(self):
        self.reqWidgets[self.requestNum][5].config(text="Enter Typeform ID")
        self.reqWidgets[self.requestNum][5].pack(padx = 3, pady = 3, fill="both", expand=True)
        self.reqWidgets[self.requestNum][0].pack(padx = 20, pady = 5, fill="both", expand=True)

    def askForSubmissionQ(self):

        formID = self.reqWidgets[self.requestNum][0].get()

        # Setting form ID as just the id code used in typeform api
        formID = formID.split(", ")[-1]

        # Updating metadata
        self.md["formID"] = formID 
        # Is self.md for data kept within the program and not sent to the server?

        # Updating data
        self.data["form_ID"] = formID
        if len(self.data["requests"]) <= self.requestNum:
            self.data["requests"].append({})
        
        # Returns list of questions with list of answers from typeform
        # self.questions, self.question_type, self.question_choices, self.question_ids = self.typeform.get_questions(formID) # get list of questions from formID
        self.questions = ["question1", "question2", "question3"]
        self.question_type = ["multiple_choice", "email", "number"]
        self.question_choices = [["choice1", "choice2", "choice3"], None, None]
        self.question_ids = ["1", "2", "3"]

        self.reqWidgets[self.requestNum][1].config(choices=self.questions)
        self.reqWidgets[self.requestNum][1].pack(padx = 20, pady = 5, fill="both", expand=True)
        self.reqWidgets[self.requestNum][5].config(text="Edit the specific form submission with the following question-response pair. Select the question (Must be a question with unique answers!):")

        
    def askForSubmissionA(self):
        qIndex = self.questions.index(self.reqWidgets[self.requestNum][1].get())
        qID = self.question_ids[qIndex]
        qType = self.question_type[qIndex]

        # Updating data
        self.data["requests"][self.requestNum]["submission_q"] = qID

        # get responses to chosen question
        # self.helperResponses = self.typeform.find_matching_form(self.md["formID"], qID)
        self.helperResponses = ["A", "B", "C", "D", "E"]

        self.reqWidgets[self.requestNum][2].config(choices=self.helperResponses)
        self.reqWidgets[self.requestNum][2].pack(padx = 20, pady = 5, fill="both", expand=True)
        
        self.reqWidgets[self.requestNum][5].config(text="Edit the specific form submission with the following question-response pair. Select the response:")

    def askForChangeQ(self):
        answer = self.reqWidgets[self.requestNum][2].get()
        self.answerIndex = self.helperResponses.index(answer)

        # Updating data
        self.data["requests"][self.requestNum]["submission_a"] = answer
        # can we just get the submission ID/number instead of question/answer to send to server?
        
        # get specific submission based on question and answer
        # ask user to choose question of the answer field they want to change        
        self.reqWidgets[self.requestNum][3].config(choices=self.questions)
        self.reqWidgets[self.requestNum][3].pack(padx = 20, pady = 5, fill="both", expand=True)
        self.reqWidgets[self.requestNum][5].config(text="Choose question field to change")

        # if going back a step
        self.nextButton.config(text="Next", command=self.nextStage)
        self.submitButton.pack_forget()

    def askForChangeA(self):
        qIndex = self.questions.index(self.reqWidgets[self.requestNum][3].get())
        qID = self.question_ids[qIndex]
        qType = self.question_type[qIndex]

        # Updating data
        self.data["requests"][self.requestNum]["change_q"] = qID

        # answer = self.typeform.find_matching_form(self.md["formID"], qID)[self.answerIndex]
        answer = "Original Answer"
        #print(answers)
        
        if qType == 'multiple_choice':
            print(answer)
            self.reqWidgets[self.requestNum][4] = AutocompleteDropdown(self.reqWidgets[self.requestNum][9], width = 50, choices=self.question_choices[qIndex])
            
        
        # NOTE: This ^ may not work if there are multiple responses.
        # Have user manually delete a duplicate from typeform first,
        # that's probably better practice anyways from an operations standpoint.

        self.reqWidgets[self.requestNum][4].pack(padx = 20, pady = 5, fill="both", expand=True)
        if qType != "multiple_choice":
            self.reqWidgets[self.requestNum][4].delete(0, tk.END)
            self.reqWidgets[self.requestNum][4].insert(-1, answer)
        self.reqWidgets[self.requestNum][5].config(text="Change response to (response type is " + qType + "):")
        self.reqWidgets[self.requestNum][5].pack(padx = 3, pady = 3, fill="both", expand=True)
        self.nextButton.config(text="Add Another Change", command=self.addRequest)
        self.submitButton.pack(side = tk.RIGHT, padx = 3, pady = 3)

    def addRequest(self):
        
        # Updating data
        self.data["requests"][self.requestNum]["change_a"] = self.reqWidgets[self.requestNum][4].get()
        self.reqWidgets[self.requestNum][4].config(state="disabled")

        self.submitButton.pack_forget()
        self.reqWidgets[self.requestNum][5].pack_forget()
        self.nextButton.config(text="Next", command=self.nextStage)
        self.requestNum += 1
        self.stage = -1
        self.initializeFields()
        self.nextStage()

    def deleteRequest(self, index):
        # delete from GUI
        print(index)
        self.reqWidgets[index][10].pack_forget() # container
        self.reqWidgets[index][7].pack_forget() # divider
        # delete from data dict and adjust requestNum
        if len(self.data["requests"]) > index:
            self.data["requests"].pop(index)
        self.requestNum -= 1
        # update each deleteButton's associated index
        for i in range(index, len(self.reqWidgets)):
            self.reqWidgets[i][6].index -= 1
        # delete from array of widgets
        self.reqWidgets.pop(index)
        # if deleted ALL requests, show initial request form
        if self.requestNum == -1:
            self.nextButton.config(text="Next", command=self.nextStage)
            self.submitButton.pack_forget()
            self.requestNum = 0
            self.stage = -1
            self.initializeFields()
            self.nextStage()
        # if deleted last (incomplete) request, but there is still at least one 
        # request, allow user to submit or add request
        elif index > self.requestNum:
            self.nextButton.config(text="Add Another Change", command=self.addRequest)
            self.nextButton.pack(side = tk.RIGHT, padx = 3, pady = 3)
            self.submitButton.pack(side = tk.RIGHT, padx = 3, pady = 3)
            self.stage = 4
            self.reqWidgets[self.requestNum][self.stage].config(state="normal")
            self.nextFunc[self.stage]()

    def submit(self):
        # Updating data
        self.data["requests"][self.requestNum]["change_a"] = self.reqWidgets[self.requestNum][4].get()
        self.reqWidgets[self.requestNum][4].config(state="disabled")

        confirmation = WrapLabel(self.scrollable, 
                                    text="Change request received. You will receive an email at " + self.data["email"] + " once the change is processed.")
        resetButton = tk.Button(self.scrollable, text = "Submit Another Request", command = self.reset)
         
        self.mainContent.destroy()
        self.bottomFrame.destroy()
        confirmation.pack(fill="both", expand=True)
        resetButton.pack(padx = 3, pady = 3)

        # send data
        print(self.data)
        # ftp = HandleFTP()
        # ftp.transfer_request(self.data)
        
    def reset(self):
        self.scrollable.destroy()
        self.scrollbar.destroy()
        self.md = {}
        self.data = {}
        self.create_widgets()

    def resetWithConfirmation(self):
        MsgBox = messagebox.askquestion ('Reset','Are you sure you want to clear all fields and restart this form?',icon = 'warning')
        if MsgBox == 'yes':
            self.reset()
        
root = tk.Tk()
app = Application(master=root)
app.mainloop() # Triggers GUI
