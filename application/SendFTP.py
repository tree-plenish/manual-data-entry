import json
import ftplib
import os
import time
"""
Class to send a json file via ftp to the server.
Right now that is linked to my ip... might have to add in paxton's backup.
This code will be built into the exe and will link front/backend.

Input a python dictionary.
Dumps into json file (stored into same folder as executed for debug... may make temporary file)
On the server, stores it in a dedicated folder tp_manual_requests.
Returns a response code or error callback.

On the server, the tp_manual_requests folder will be periodically checked
and any json requests in there will be processed and moved to a completed
folder for reference.
"""

class HandleFTP:

    def __init__(self, data):

        self.data = data
        
        
        # Text file with my ip... please don't make this public
        if os.path.exists("/home/justinmiller/Desktop/ip.txt"):
            key_file = "/home/justinmiller/Desktop/ip.txt"

        else:
            key_file = input("Enter full address of api key text file")


        # Input my password
        self.user = input("Enter User Name: ")
        self.password = input("Enter Password for User: ")
        

        # Getting ip (as str). Txt files reading weird again, hold to 10 digits for now.
        self.server_ip = open(key_file, "r").read()[:10]

    def create_json_from_dict(self):

        self.time_requested = str(int(time.time())) # Note, create json must be called before save manual data
        temp_file = self.time_requested + ".json"
        
        with open(temp_file, "w") as outfile: 
            json.dump(self.data, outfile)

                              
    def get_ftp_object(self):

        ftp = ftplib.FTP()
        ftp.connect(self.server_ip, 21)
        ftp.login(self.user, self.password)

        return ftp

    def save_manual_data(self, ftp):

        # Full path to manual data folder (using user)
        path = "/home/" + self.user + "/Documents/tp_manual_requests/"

        # TODO (OPTIONAL)... add email to filename instead of just timestamp
        file_name = self.time_requested + ".json"

        # Moving to path location
        ftp.cwd(path)

        # Uploading file
        ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))

        
        
h = HandleFTP({"Name":"Example Request", "Request Number" : 0})
h.create_json_from_dict()
ftp = h.get_ftp_object()
h.save_manual_data(ftp)
