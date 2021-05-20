import tkinter as tk
from customWidgets import AutocompleteDropdown

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Test window")
        self.master.geometry("500x300")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.questions = ['C','C++','Java', 'Python','Perl',
                               'PHP','ASP','JS', 'test2', 'test3', 
                            'test1', 'test4', 'test5', 'test6' ] # get list of questions from formID
        self.searchBox = AutocompleteDropdown(self.master, choices=self.questions)
        self.searchBox.pack()


root = tk.Tk()
app = Application(master=root)
app.mainloop() # Triggers GUI
