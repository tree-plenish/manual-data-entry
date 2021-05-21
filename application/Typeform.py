import numpy as np
import requests
import os

class Typeform:

    def __init__(self, **kwargs):

        # Path to Typeform API Key (Primary works on Tree-Plenish Server)
        if os.path.exists("/home/justinmiller/Desktop/typeformId.txt"):
            key_file = "/home/justinmiller/Desktop/typeformId.txt"
        elif os.path.exists("C:/Users/cntaw/desktop/tree plenish/typeformId.txt"):
            key_file = "C:/Users/cntaw/desktop/tree plenish/typeformId.txt"
        else:
            key_file = input("Enter full address of api key text file")


        # Loading key into workspace [removing ending whitespace if applicable]
        self.api_key = open(key_file, "r").read()
        self.api_key = self.api_key[:44]

        # Loading header dict
        self.headers = {"Authorization": "Bearer " + self.api_key}


    def get_all_forms(self):

        # Limited to 200 for just getting forms, 2000 for responses. Double check before changing.
        page_size = 92

        # Getting first page of results and checking for success
        result = requests.get("https://api.typeform.com/forms", params={"page_size": page_size}, headers=self.headers)
        assert (result.status_code == 200), "A " + str(result.status_code) + " error occurred"

        # Getting dict and md
        result_dict = result.json()
        self.total_forms = result_dict['total_items']
        self.total_pages = result_dict['page_count']
        forms = result_dict['items']

        
        # Looping through pages extending item list
        for page in range(2, self.total_pages + 1):

            # Getting result
            result = requests.get("https://api.typeform.com/forms", params={"page_size": page_size, "page": page},
                                  headers=self.headers)

            # Getting dict and md
            result_dict = result.json()

            # Appending
            forms = forms + result_dict['items']
            

        return forms

    def get_form_titles(self, forms):

        return [form["title"] for form in forms]
        
"""
# EXAMPLE CALLS
# init()... will run on import
# Will ask for a file input on any computer but the server
# Input the full path to the api key text file, including file name
t = Typeform()

# Getting all forms with content currently in the account
# Returns a list of dicts with all of the info that is used later
forms = t.get_all_forms()

# Quick list comprehension to get a list of all titles from a forms list
titles = t.get_form_titles(forms)
"""
