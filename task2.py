import wget
import os
import pandas as pd
import io

# initialize lists for employee names and timestamps for mails
employee_names = []
employee_timestamps = []

# Collecting timestamp from mail
def mail_timestamp(path):
    with io.open(path, "r", encoding="ISO-8859-1") as file:
        content = file.readlines()
        timestamp = content[1].lstrip("Date: ").rstrip("\n") # storing timestamp
        file.close()
        return timestamp

# function to go through inbox folder
def inbox_folder(path, nickname):
    # ensuring that the path is a directory
    if os.path.isdir(path):
        # Check if the user has any inbox folder
        if "inbox" in os.listdir(path):
            inbox_mail = os.path.join(path, "inbox") # path to inbox folder in directory
            mails = os.listdir(inbox_mail) # list of mail files

            for mail in mails:
                mail_file_path = os.path.join(inbox_mail,mail)
                if not os.path.isdir(mail_file_path):
                    timestamp = mail_timestamp(mail_file_path)
                # append employee nickname and timestamp of each recived mail
                    employee_names.append(nickname)
                    employee_timestamps.append(timestamp)

# Go through each folder, or email user and run function for inbox mail folder for each
for sender_folder in os.listdir("./maildir/"):
    inbox_folder(os.path.join("./maildir/", sender_folder), sender_folder)

# get DataFrame of employee name and time of recieved email
employee_inbox_times = pd.DataFrame({"employee": employee_names,
                                     "time": employee_timestamps})

# create week day column
employee_inbox_times["weekday"] = [i.split(",")[0] for i in employee_inbox_times["time"]]

