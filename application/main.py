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
        scrollable = tk.Canvas(self.master)
        scrollable.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=scrollable.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure scrollable canvas
        scrollable.configure(yscrollcommand=scrollbar.set)

        innerFrame = tk.Frame(scrollable)
        scrollable.height = scrollable.winfo_reqheight()
        scrollable.width = scrollable.winfo_reqwidth()
        scrollable.create_window((0,0), window=innerFrame, anchor="nw", width=scrollable.width)
        scrollable.addtag_all("resize")
        # allow mousewheel to scroll
        scrollable.bind_all("<MouseWheel>", lambda e: scrollable.yview_scroll(-1 * int((e.delta / 120)), "units"))
        

        # resize content window width in canvas when window is resized
        # also attach scroll region to scroll bar
        def resizeAndSetScroll(e):
            scrollable.scale("resize",0,0,float(e.width)/scrollable.width,float(e.height)/scrollable.height)
            scrollable.width = e.width
            scrollable.height = e.height
            scrollable.configure(scrollregion=scrollable.bbox("all"))
        
        scrollable.bind("<Configure>", resizeAndSetScroll)

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
        self.emailLabel.pack(padx = 5, pady = 5)
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

        if self.entryPtDropdown.get() == "Typeform":

            self.entryPtDropdown.config(state="disabled")
            self.emailEntry.config(state="disabled")
            self.typeDropdown.config(state="disabled")

            self.typeform = Typeform()

            self.prevButton = tk.Button(self.bottomFrame, text = "Back", command = self.prevStage)
            self.prevButton.pack(side = tk.LEFT, padx = 3, pady = 3)
            self.nextButton = tk.Button(self.bottomFrame, text = "Next", command = self.nextStage)
            self.nextButton.pack(side = tk.RIGHT, padx = 3, pady = 3)


            # initialize typeform related widgets
            self.stageText = WrapLabel(self.leftFrame, text="")
            self.formIDBox = AutocompleteDropdown(self.rightFrame,width = 50, choices=[])
            # load all forms once here (takes a while, and likely will not change if user clicks back button)
            forms = []
            for form in self.typeform.get_all_forms():
                forms.append(form["title"] + ", " + form["id"])
            self.formIDBox.config(choices=forms)
            self.submissionQBox = AutocompleteDropdown(self.rightFrame, width = 50, choices=[])
            self.submissionABox = AutocompleteDropdown(self.rightFrame, width = 50, choices=[])
            self.changeQBox = AutocompleteDropdown(self.rightFrame, width = 50, choices=[])
            self.changeABox = tk.Entry(self.rightFrame, width = 50)
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
                    messagebox.showerror("Error", "Please select one of the options listed.")
                    return
            self.stage += 1
            self.nextFunc[self.stage]()
        self.fields[self.stage].config(state="normal")
        if self.stage > 0:
            self.fields[self.stage-1].config(state="disabled")


    def prevStage(self):
        if self.stage > 0:
            self.stage -= 1
            self.nextFunc[self.stage]()
        self.fields[self.stage].config(state="normal")
        if self.stage < len(self.nextFunc)-1:
            self.fields[self.stage+1].config(state="disabled")

    def askForFormID(self):
        self.stageText.config(text="Enter Typeform ID")
        self.stageText.pack(padx = 3, pady = 3, fill="both", expand=True)
        self.formIDBox.pack(padx = 20, pady = 5, fill="both", expand=True)

    def askForSubmissionQ(self):
        formID = self.formIDBox.get()

        # Setting form ID as just the id code used in typeform api
        formID = formID.split(", ")[-1]

        # Updating metadata
        self.md["formID"] = formID
        
        # Returns list of questions with list of answers from typeform
        self.questions, self.question_type, self.question_choices, self.question_ids = self.typeform.get_questions(formID) # get list of questions from formID

        self.submissionQBox.config(choices=self.questions)
        self.submissionQBox.pack(padx = 20, pady = 5, fill="both", expand=True)
        self.stageText.config(text="Edit the specific form submission with the following question-response pair. Select the question:")

        
    def askForSubmissionA(self):
        qIndex = self.questions.index(self.submissionQBox.get())
        qID = self.question_ids[qIndex]
        qType = self.question_type[qIndex]

        # get responses to chosen question
        self.helperResponses = self.typeform.find_matching_form(self.md["formID"], qID)
        self.submissionABox.config(choices=self.helperResponses)
        self.submissionABox.pack(padx = 20, pady = 5, fill="both", expand=True)
        
        self.stageText.config(text="Edit the specific form submission with the following question-response pair. Select the response:")

    def askForChangeQ(self):
        answer = self.submissionABox.get()
        self.answerIndex = self.helperResponses.index(answer)
        
        # get specific submission based on question and answer
        # ask user to choose question of the answer field they want to change        
        self.changeQBox.config(choices=self.questions)
        self.changeQBox.pack(padx = 5, pady = 5, fill="both", expand=True)
        self.stageText.config(text="Choose question field to change")

    def askForChangeA(self):
        qIndex = self.questions.index(self.changeQBox.get())
        qID = self.question_ids[qIndex]
        qType = self.question_type[qIndex]

        answer = self.typeform.find_matching_form(self.md["formID"], qID)[self.answerIndex]
        #print(answers)
        
        if qType == 'multiple_choice':
            print(answer)
            self.changeABox = AutocompleteDropdown(self.rightFrame, width = 50, choices=self.question_choices[qIndex])
            
        
        # NOTE: This ^ may not work if there are multiple responses.
        # Have user manually delete a duplicate from typeform first,
        # that's probably better practice anyways from an operations standpoint.

        self.changeABox.pack(padx = 20, pady = 5, fill="both", expand=True)
        if qType != "multiple_choice":
            self.changeABox.insert(-1, answer)
        self.stageText.config(text="Change response to (response type is " + qType + "):")

        self.nextButton.config(text="Submit", command=self.submit)

    def submit(self):
        request = {
            "email" : self.emailEntry.get(),
            "type" : self.typeDropdown.get(),
            "entry_point" : self.entryPtDropdown.get(),
            "form_id" : self.formIDBox.get(),
            "submission_q" : self.submissionQBox.get(),
            "submission_a" : self.submissionABox.get(),
            "change_q" : self.changeQBox.get(),
            "change_a" : self.changeABox.get()
        }
        print(request)
        self.mainContent.destroy()
        self.bottomFrame.destroy()
        self.confirmation = WrapLabel(self.master, 
                                    text="Change request received. You will receive an email at " + request["email"] + " once the change is processed.")
        self.confirmation.pack(fill="both", expand=True)


root = tk.Tk()
app = Application(master=root)
app.mainloop() # Triggers GUI
