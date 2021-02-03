import wget
import os
import pandas as pd
import sys

# handling script arguments
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

# Initialize global lists which will be used to build the data set of emails

# global lists for sender data frame
sender_paths = []
sender_senders = []
sender_timestamps = []

# global lists for recipient data frame
recipients_paths = []
recipients = []
recipients_timestamps = []

# function to run through a _sent_mail folder in the folder structure
def sent_mail_folder(path):
    # ensuring that the path is a directory
    if os.path.isdir(path):
        # Check if the user has sent mails
        if "_sent_mail" in os.listdir(path):
            sent_mail = os.path.join(path, "_sent_mail")  # path to _sent_mail folder in directory
            mails = os.listdir(sent_mail)  # list of mail files

            for mail in mails:
                mail_file_path = os.path.join(sent_mail, mail)
                sender, to_s, bcc_s, timestamp = one_mail_check(mail_file_path)

                # append sender information
                sender_paths.append(mail_file_path)
                sender_senders.append(sender)
                sender_timestamps.append(timestamp)

                # append recipient information

                # first we append To: recipients to lists
                for to_rec in to_s:
                    recipients_paths.append(mail_file_path)
                    recipients.append(to_rec)
                    recipients_timestamps.append(timestamp)

                # if there are CCs we append those as well
                if bcc_s:
                    for bcc_rec in bcc_s:
                        recipients_paths.append(mail_file_path)
                        recipients.append(bcc_rec)
                        recipients_timestamps.append(timestamp)


# Collecting information from one mail
def one_mail_check(path):
    with open(path, "r") as file:
        content = file.readlines()
        timestamp = content[1].lstrip("Date: ").rstrip("\n")  # storing timestamp

        # storing sender
        if content[2].startswith("From: "):
            mail_sender = content[2].lstrip("From: ").rstrip("\n")

        # counters to prevent reading duplicates
        to_count = 0
        bcc_count = 0

        # initialize recipients
        to_s = []
        bcc_s = []

        # listing recipients
        for i, line in enumerate(content):
            if line == "\n":  # break if the content block has been read
                break
            # check to
            if line.startswith("To:") and to_count == 0:
                to_s = line.lstrip("To: ").rstrip(" \n").split(",")
                to_count += 1
                to_index = i + 1
                while not content[to_index].startswith("Subject"):
                    content[to_index].strip().rstrip(" \n").split(",")
                    to_s = to_s + content[to_index].strip().rstrip(" \n").split(",")
                    to_index += 1
                to_s = [i for i in to_s if i]  # remove all empty strings

            # check bcc, assuming all bcc:s are in cc:s
            if line.startswith("Bcc:") and bcc_count == 0:
                bcc_s = bcc_s + line.lstrip("Bcc: ").rstrip(" \n").split(", ")
                bcc_count += 1
                bcc_index = i + 1
                while not content[bcc_index].startswith("X-"):
                    content[bcc_index].strip().rstrip(" \n").split(",")
                    bcc_s = bcc_s + content[bcc_index].strip().rstrip(" \n").split(",")
                    bcc_index += 1
                bcc_s = [i for i in bcc_s if i]  # remove all empty strings
        file.close()

    return mail_sender, to_s, bcc_s, timestamp


# Go through each folder, or email user, and run function for each _sent_mail folder
for sender_folder in os.listdir("./maildir/"):
    sent_mail_folder(os.path.join("./maildir/", sender_folder))

# create dataframes for sender and recipient data
sender_df = pd.DataFrame({"id": sender_paths, "sender": sender_senders, "time": sender_timestamps})
recipient_df = pd.DataFrame({"id": recipients_paths, "recipient": recipients, "time": recipients_timestamps})

# FIRST TASK 1)

# merging data frames in order to get sender for each each recipient, left joining on filepath (id)
merged_df = pd.merge(recipient_df, sender_df, how="left", on="id")

# aggregate and obtain mail counts for each sender-recipient pair
mail_counts = merged_df.groupby(by=["recipient", "sender"]).size()

# convert to DataFrame and write to csv
grouped = pd.DataFrame({"count": mail_counts}).reset_index()
grouped = grouped[["sender", "recipient", "count"]]

grouped.to_csv("./emails_sent_totals.csv")
print("emails_sent_totals.csv created!")

