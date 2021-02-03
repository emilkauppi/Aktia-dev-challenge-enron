# Aktia-dev-challenge-enron
Aktia dev challenge for summer intern junior data engineer applicants. Done by Emil Kauppi.  

This following challenge was done for Aktia Junior Data Engineer Intern position. The data set used is from https://www.cs.cmu.edu/~./enron/
and features the Enron Email Dataset.

The challenge includes two tasks. First task is to compute amount of sent emails from each sender to a any recipient and return
the counts in a .csv. The resulting .csv is titled _emails_sent_totals.csv_. The second task is to count average of received emails per week day per employee and return the result
as a .csv file. The resulting .csv is titled *emails_sent_average_per_weekday*. 

The challenge was how to deal with the large data set properly. I decided to assume that the data set needs to be
downloaded locally and dealt with locally. However, the data cannot be pushed to Github which is why there is a download option and extracting
in order to make the data included available. First download of data takes long (over 1Gb). Hence, if there is no dataset in the cloned directory, the download option should be chosen. If
you have the data in place as a ".tar" file, it needs to be extracted, which the script can do. Extracting the data also takes time. Without any options
the scripts assume the "maildir" dataset folder being located in the root of the cloned directory. It looks for the .tar file of the dataset, if it is not found, 
you are in trouble :)  

The scripts can be run from the command line by running a regular python script. The script names indicate which of the tasks is run.

For the first task the script is run by executing (on MacOS)

`python3 task1.py`

in the working directory, the cloned root folder.

Similarily, for the second task run

`python3 task2.py`

These will output the wanted .csv files to the working directory. If the dataset is needed to be to downloaded then a download option needs to be inserted
meaning typing "D" as a script argument. That is run,

`python3 task1.py D`  or 

`python3 task2.py D`

The script then downloads the data and extracts the "maildir" folder, which is required. 

Additionally, this git includes the latest .csv files for both tasks.

After extracting the dataset (having the _maildir_ folder in place) the tasks and the outputs are produced
somewhat quickly. There are still probably plenty of things to improve and the .tar file could probably be read
using the python's  _tarfile_ module in order to read only necessary data. This was probably something that was hinted in 
the challenge description. However,
this was a quick solution for the tasks at hand and included plenty of things I was not that familiar with. 

Thank you, a very interesting and educating task! 

