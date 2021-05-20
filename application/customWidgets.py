import tkinter as tk

class AutocompleteDropdown(tk.Frame):
    def __init__(self, parent, **options):
        self._choices = options.pop("choices") # autocomplete choices
        tk.Frame.__init__(self, parent, **options)

        #creating text box 
        self._searchBox = tk.Entry(self)
        self._searchBox.pack(anchor=tk.NW, fill='x')
        self._searchBox.bind('<KeyRelease>', self._checkkey)

        # to do: hide/show list box like combobox?
        # self._searchBox.bind('<ButtonPress-1>', self.toggleList)
        
        listFrame = tk.Frame(self)
        listFrame.pack(fill = tk.BOTH)

        #creating list box
        self._lb = tk.Listbox(listFrame)
        self._lb.pack(side = tk.LEFT, fill = tk.BOTH)
        self._lb.bind("<<ListboxSelect>>", self._updateEntry)

        # scrollbar for list box
        self._scrollbar = tk.Scrollbar(listFrame)
        self._scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)

        self._lb.config(yscrollcommand = self._scrollbar.set)
        self._scrollbar.config(command = self._lb.yview)

        self._updateListbox(self._choices)
    
    def _checkkey(self, event):
        # update choices whenever user types in entry
        value = self._searchBox.get()
        if value == '':
            data = self._choices
        else:
            data = []
            for item in self._choices:
                if value.lower() in item.lower():
                    data.append(item)
        # update data in listbox
        self._updateListbox(data)

    def _updateEntry(self, event):
        # update entry text if user selects something from listbox
        selection = self._lb.curselection()
        if selection:
            self._searchBox.delete(0,tk.END)
            self._searchBox.insert(0,self._lb.get(selection))
        self._checkkey(None)

    def _updateListbox(self, data):
        # update listbox based on what user types in entry
        # clear previous data
        self._lb.delete(0, 'end')
        # put new data
        for item in data:
            self._lb.insert('end', item)
    
    def config(self, **options):
        newChoices = options.pop("choices") # autocomplete choices
        tk.Frame.config(self, **options) # check this
        self._searchBox.delete(0,tk.END)
        self._choices = newChoices
        self._updateListbox(self._choices)

    def get(self):
        return self._searchBox.get()


class WrapLabel(tk.Label):
    # automatically adjusts text wrapping with window resize
    def __init__(self, master=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))