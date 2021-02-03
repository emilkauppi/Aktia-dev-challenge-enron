import wget
import os
import pandas as pd
import io
import sys

# Handling script arguments
if len(sys.argv) > 1:
    if sys.arg[1] == "D":
        url = "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz"
        wget.download(url)

# If the .tar file is not extracted -> extracts locally, results in maildir folder
if not os.path.exists("./maildir"):
    if os.path.exists("./enron_mail_20150507.tar.gz"):
        file = tarfile.open("enron_mail_20150507.tar")
        file.extractall("./")
        file.close()
    if os.path.exists("./enron_mail_20150507.tar"): # if no .gz
        file = tarfile.open("enron_mail_20150507.tar")
        file.extractall("./")
        file.close()
    else:
        print("There required files are not in place!")

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

# preprocessing done to get time into datetime format
employee_inbox_times["date"] = [i[0:16] for i in employee_inbox_times["time"]] # transform initial timestamp to date friendly format
employee_inbox_times["date"] = pd.to_datetime(employee_inbox_times["date"], errors="coerce") # transform into datetime
employee_inbox_times = employee_inbox_times.dropna() # drop NaN values, just in case, would need debugging
employee_inbox_times["day_of_week"] = employee_inbox_times["date"].dt.dayofweek # create day_of_week column

# aggregate by first computing email for each day, per employee and then average out of those per day of week
emails_count_per_day = pd.DataFrame(employee_inbox_times.groupby(by=["employee", "date"]).size()).reset_index() # emails per day per employee
emails_count_per_day["day_of_week"] = emails_count_per_day["date"].dt.dayofweek
email_averages = emails_count_per_day.groupby(by=["employee","day_of_week"]).mean() # mean of the amounts
email_averages = email_averages.rename(columns ={0: "avg_count"}) # rename columns


# write .csv
email_averages.to_csv("./emails_sent_average_per_weekday.csv")
print("emails_sent_average_per_weekday.csv created!")
