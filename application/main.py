import _tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from Typeform import Typeform
from customWidgets import AutocompleteDropdown, WrapLabel

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Tree Plenish Manual Data Entry")
        self.master.geometry("500x500")
        self.pack()
        self.create_widgets()

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

        scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.scrollable.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure scrollable canvas
        self.scrollable.configure(yscrollcommand=scrollbar.set)

        innerFrame = tk.Frame(self.scrollable)
        self.scrollable.height = self.scrollable.winfo_reqheight()
        self.scrollable.width = self.scrollable.winfo_reqwidth()
        self.scrollable.create_window((0,0), window=innerFrame, anchor="nw", width=self.scrollable.width)
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

        ## End scrollbar for window

        self.label = tk.Label(innerFrame, text = "Tree Plenish Manual Data Entry")
        self.label.pack()

        self.mainContent = tk.Frame(innerFrame)
        self.mainContent.pack()
        self.mainContent.grid_columnconfigure(0, weight=1, uniform="group1")
        self.mainContent.grid_columnconfigure(1, weight=2, uniform="group1")
        self.mainContent.grid_rowconfigure(0, weight=1)

        self.leftFrame = tk.Frame(self.mainContent)
        self.rightFrame = tk.Frame(self.mainContent)

        self.leftFrame.grid(row=0, column=0, sticky="nsew")
        self.rightFrame.grid(row=0, column=1, sticky="nsew")

        self.bottomFrame = tk.Frame(innerFrame)
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

        self.entryPtDropdown.bind("<<ComboboxSelected>>", self.setAdditionalOptions)

        self.stage = -1
        self.nextFunc = [self.askForFormID, self.askForSubmissionQ, self.askForSubmissionA, self.askForChangeQ, self.askForChangeA, self.submit]
        self.fields = []
        # self.submitButton = tk.Button(self.bottomFrame, text = "Submit", command = self.retrieveData)
        # self.submitButton.pack(padx = 3, pady = 3)        

    

    def setAdditionalOptions(self, event):
        if self.entryPtDropdown.get() == "" or self.emailEntry.get() == "" or self.typeDropdown.get() == "":
            messagebox.showerror("Error", "Please fill in all required fields")
            # to do: email validation?
            return

        self.data["email"] = self.emailEntry.get()
        self.data["type"] = self.typeDropdown.get()
        self.data["entry_point"] = self.entryPtDropdown.get()

        if self.data["entry_point"] == "Typeform" and self.data["type"] == "Modify":
            self.requestNum = 0
            self.data["requests"] = [] # array of changes the user wants to make to a form

            self.entryPtDropdown.config(state="disabled")
            self.emailEntry.config(state="disabled")
            self.typeDropdown.config(state="disabled")

            self.typeform = Typeform()

            self.prevButton = tk.Button(self.bottomFrame, text = "Back", command = self.prevStage)
            self.prevButton.pack(side = tk.LEFT, padx = 3, pady = 3)
            self.nextButton = tk.Button(self.bottomFrame, text = "Next", command = self.nextStage)
            self.nextButton.pack(side = tk.RIGHT, padx = 3, pady = 3)
            self.submitButton = tk.Button(self.bottomFrame, text = "Submit", command = self.submit)

            
            # load all forms once here (takes a while, and likely will not change if user clicks back button or requests multiple changes)
            self.forms = []
            for form in self.typeform.get_all_forms():
                self.forms.append(form["title"] + ", " + form["id"])

            self.initializeFields()
            
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
    def initializeFields(self):
        ttk.Separator(self.rightFrame,orient='horizontal').pack(fill='x', pady=8)
        #currently for typeform changes only
        formIDBox = AutocompleteDropdown(self.rightFrame,width = 50, choices=[])
        formIDBox.config(choices=self.forms)
        submissionQBox = AutocompleteDropdown(self.rightFrame, width = 50, choices=[])
        submissionABox = AutocompleteDropdown(self.rightFrame, width = 50, choices=[])
        changeQBox = AutocompleteDropdown(self.rightFrame, width = 50, choices=[])
        changeABox = tk.Entry(self.rightFrame, width = 50)

        stageText = WrapLabel(self.leftFrame, text="")
        self.fields.append([formIDBox, submissionQBox, submissionABox, changeQBox, changeABox, stageText])

    def nextStage(self):
        if self.stage < len(self.nextFunc)-1:
            if isinstance(self.fields[self.requestNum][self.stage], AutocompleteDropdown):
                if not self.fields[self.requestNum][self.stage].verify():
                    # pop up error
                    messagebox.showerror("Error", "Please select one of the options listed.")
                    return
            self.stage += 1
            self.nextFunc[self.stage]()
        self.fields[self.requestNum][self.stage].config(state="normal")
        if self.stage > 0:
            self.fields[self.requestNum][self.stage-1].config(state="disabled")


    def prevStage(self):
        if self.stage > 0:
            self.stage -= 1
            self.nextFunc[self.stage]()
        self.fields[self.requestNum][self.stage].config(state="normal")
        if self.stage < len(self.nextFunc)-1:
            self.fields[self.requestNum][self.stage+1].config(state="disabled")

    def askForFormID(self):
        self.fields[self.requestNum][5].config(text="Enter Typeform ID")
        self.fields[self.requestNum][5].pack(padx = 3, pady = 3, fill="both", expand=True)
        self.fields[self.requestNum][0].pack(padx = 20, pady = 5, fill="both", expand=True)

    def askForSubmissionQ(self):

        formID = self.fields[self.requestNum][0].get()

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
        self.questions, self.question_type, self.question_choices, self.question_ids = self.typeform.get_questions(formID) # get list of questions from formID

        self.fields[self.requestNum][1].config(choices=self.questions)
        self.fields[self.requestNum][1].pack(padx = 20, pady = 5, fill="both", expand=True)
        self.fields[self.requestNum][5].config(text="Edit the specific form submission with the following question-response pair. Select the question (Must be a question with unique answers!):")

        
    def askForSubmissionA(self):
        qIndex = self.questions.index(self.fields[self.requestNum][1].get())
        qID = self.question_ids[qIndex]
        qType = self.question_type[qIndex]

        # Updating data
        self.data["requests"][self.requestNum]["submission_q"] = qID

        # get responses to chosen question
        self.helperResponses = self.typeform.find_matching_form(self.md["formID"], qID)
        self.fields[self.requestNum][2].config(choices=self.helperResponses)
        self.fields[self.requestNum][2].pack(padx = 20, pady = 5, fill="both", expand=True)
        
        self.fields[self.requestNum][5].config(text="Edit the specific form submission with the following question-response pair. Select the response:")

    def askForChangeQ(self):
        answer = self.fields[self.requestNum][2].get()
        self.answerIndex = self.helperResponses.index(answer)

        # Updating data
        self.data["requests"][self.requestNum]["submission_a"] = answer
        # can we just get the submission ID/number instead of question/answer to send to server?
        
        # get specific submission based on question and answer
        # ask user to choose question of the answer field they want to change        
        self.fields[self.requestNum][3].config(choices=self.questions)
        self.fields[self.requestNum][3].pack(padx = 20, pady = 5, fill="both", expand=True)
        self.fields[self.requestNum][5].config(text="Choose question field to change")

        # if going back a step
        self.nextButton.config(text="Next", command=self.nextStage)
        self.submitButton.pack_forget()

    def askForChangeA(self):
        qIndex = self.questions.index(self.fields[self.requestNum][3].get())
        qID = self.question_ids[qIndex]
        qType = self.question_type[qIndex]

        # Updating data
        self.data["requests"][self.requestNum]["change_q"] = qID

        answer = self.typeform.find_matching_form(self.md["formID"], qID)[self.answerIndex]
        #print(answers)
        
        if qType == 'multiple_choice':
            print(answer)
            self.fields[self.requestNum][4] = AutocompleteDropdown(self.rightFrame, width = 50, choices=self.question_choices[qIndex])
            
        
        # NOTE: This ^ may not work if there are multiple responses.
        # Have user manually delete a duplicate from typeform first,
        # that's probably better practice anyways from an operations standpoint.

        self.fields[self.requestNum][4].pack(padx = 20, pady = 5, fill="both", expand=True)
        if qType != "multiple_choice":
            self.fields[self.requestNum][4].insert(-1, answer)
        self.fields[self.requestNum][5].config(text="Change response to (response type is " + qType + "):")
        self.fields[self.requestNum][5].pack(padx = 3, pady = 3, fill="both", expand=True)
        self.nextButton.config(text="Add Another Change", command=self.addRequest)
        self.submitButton.pack(side = tk.RIGHT, padx = 3, pady = 3)

    def addRequest(self):

        # Updating data
        self.data["requests"][self.requestNum]["change_a"] = self.fields[self.requestNum][4].get()
        self.fields[self.requestNum][4].config(state="disabled")

        self.submitButton.pack_forget()
        self.fields[self.requestNum][5].pack_forget()
        self.nextButton.config(text="Next", command=self.nextStage)
        self.requestNum += 1
        self.stage = -1
        self.initializeFields()
        self.nextStage()


    def submit(self):
        self.confirmation = WrapLabel(self.scrollable, 
                                    text="Change request received. You will receive an email at " + self.data["email"] + " once the change is processed.")
        self.mainContent.destroy()
        self.bottomFrame.destroy()
        self.confirmation.pack(fill="both", expand=True)

        # send data
        print(self.data)

root = tk.Tk()
app = Application(master=root)
app.mainloop() # Triggers GUI
