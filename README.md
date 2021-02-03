# Aktia-dev-challenge-enron
Aktia dev challenge for summer intern junior data engineer applicants. 

Following task was done for Aktia Junior Data Engineer Intern position. The data set used is from https://www.cs.cmu.edu/~./enron/.

The challenge includes two tasks. First task is to compute amount of sent emails from each sender to a any recipient and return
the counts in a .csv. The second task was to count average of received emails per week day per employee and return the result
as a .csv file. The challenge was how to deal with the large data set properly. I decided to assume that the data set needs to be
downloaded locally and dealt with locally. However, the data cannot be pushed to Github which is why there is a download option and extracting
option, in order to make this available. That is, if there is no data set in the cloned directory, the download option should be chosen. If
you have the data set as the ".tar" file, it needs to be extracted, which the script can do with proper option. Without any options
the scripts assume the "maildir" dataset folder being located in the cloned directory. 

The scripts can be run from the command line by running a regular python script. The script names indicate which task of the tasks are run.

For the first task the script is run by executing 

`python3 task1.py`

in the working directory. 

Similarily, for the second task

`python3 task2.py`

These will output the wanted .csv files to the working directory. If the data set is required to download then a download option needs to be inserted

`python3 task1.py D` or `python3 task2.py D`. The script checks then for "maildir" folder and extracts from the downloaded data set file, if not found. 

Also, this git includes the latest .csv files for both tasks. 

