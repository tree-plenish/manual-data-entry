import numpy as np
import requests
import os

class Typeform:

    def __init__(self, **kwargs):

        # Path to Typeform API Key (Primary works on Tree-Plenish Server)
        if os.path.exists("/home/justinmiller/Desktop/typeformId.txt"):
            key_file = "/home/justinmiller/Desktop/typeformId.txt"

        else:
            key_file = input("Enter full address of api key text file")


        # Loading key into workspace [removing ending whitespace if applicable]
        self.api_key = open(key_file, "r").read()
        self.api_key = self.api_key[:44]

        # Loading header dict
        self.headers = {"Authorization": "Bearer " + self.api_key}

    ###############################
    # GET ALL FORMS FUNCTIONALITY #
    ###############################
    
    def get_all_forms(self):

        # Limited to 200 for just getting forms, 2000 for responses. Double check before changing.
        page_size = 100

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

    ##################################
    # GET FORM CONTENT FUNCTIONALITY #
    ##################################
    
    def get_questions(self, form_id):

        # Getting form details
        result = requests.get("https://api.typeform.com/forms/" + form_id, headers=self.headers)

        # Asserting successful request
        assert (result.status_code == 200), "A " + str(result.status_code) + " error occurred"

        # Getting form response as a dict
        form_content = result.json()

        # Loop through fields recording title and id of each question
        questions = []
        question_ids = []
        question_type = []
        question_choices = []
        for field in form_content["fields"]:

            questions.append(field["title"])
            question_type.append(field["type"])
            question_ids.append(field["id"])

            mc_options = None
            if field["type"] == "multiple_choice":

                mc_options = [choice["label"] for choice in field["properties"]["choices"]]

            question_choices.append(mc_options)
            
        return questions, question_type, question_choices, question_ids

    def get_answers(self, form_id):
    
         # Gets 1 answer response (we can pull sample answers)
        result = requests.get("https://api.typeform.com/forms/" + form_id + "/responses", params={"page_size": 1000},
                                  headers=self.headers)
        
        # Asserting successful request
        assert (result.status_code == 200), "A " + str(result.status_code) + " error occurred"
        
        # Getting answers response as a dict
        all_responses = result.json()
        
        # Asserting less than 1000 responses to the form
        assert (all_responses["page_count"] == 1), "WARNING: Only 1000 most recent responses retrieved"

        # RESPONSE NUMBER: ADD A FUNCTION TO GET THIS IN
        response_num = 0
        response_content = all_responses["items"][response_num]["answers"]

        # Loop through filds recording answer and id (to link with question)
        answers = []
        answer_ids = []
        for response in response_content:

            response_type = response["type"]

            # Answer handling... some mc questions give labeled answers
            answer = response[response_type]
            
            if type(answer) is dict:
                try:
                    answer = answer["label"]
                except:
                    answer = "Type Issue: May be payment confirmation"
                
            answers.append(answer)
            answer_ids.append(response["field"]["id"])

        # Getting dict of md (just submission time for now)
        md = {}
        md["submission_time"] = all_responses["items"][response_num]["submitted_at"]
        
        return answers, answer_ids, md

    def find_matching_form(self, form_id, question_id):

        # Gets 1 answer response (we can pull sample answers)
        # Should probably make this class var so it isn't run twice
        # Maybe even run it in itit... though that would slow down tkinter boot
        result = requests.get("https://api.typeform.com/forms/" + form_id + "/responses", params={"page_size": 1000},
                                  headers=self.headers)

        # Asserting successful request
        assert (result.status_code == 200), "A " + str(result.status_code) + " error occurred"
        
        # Getting answers response as a dict
        all_responses = result.json()

        # Looping thorough each response, recording answer to the question
        num_responses = all_responses["total_items"]

        # Looping through responses getting the answer to the chosen question
        possible_answers = [] 
        for response in all_responses["items"]:

            # Getting answer content
            answers = response["answers"]

            # For each response get the index of the chosen question
            chosen_index = None
            for answer_num in range(len(answers)):

                answer_id = answers[answer_num]["field"]["id"]
                if answer_id == question_id:

                    chosen_index = answer_num
                    break

            # Make sure we found our index
            assert (answer_num is not None), "ID Error, no answer found for question id"

            
            answer_content = answers[chosen_index]
            possible_answers.append(answer_content[answer_content["type"]])
            
        return possible_answers


# t = Typeform()
# questions, question_type, question_choices, question_ids = t.get_questions("VUkfEM0w")
# answers, answer_ids, md = t.get_answers("VUkfEM0w")
# possible_answers = t.find_matching_form("VUkfEM0w", question_ids[3]) # the question id points to the email 
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

# Getting list of questions in a form id
questions, question_type, question_choices, question_ids = t.get_questions(form_id) # form_id can be found from the forms dict

# Getting list of answers in a form id
answers, answer_ids, md = t.get_questions(form_id) # form_id can be found from the forms dict

# Getting a list of possible answers to a question to use as an identifier
possible_answers = t.find_matching_form(form_id, question_id) # the question id points to the email 


# OTHER NOTES
# I've been building this around question ids a lot because some people answers
# may be left blank, potentially screwing up indexing. Try to always reference
# to the id when working between questions and answers.
"""
