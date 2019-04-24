# manage-gmail-labels

This is a python command line tool to manage Gmail labels, i.e. creating, deleting, removing. It does not perform any operations over emails as of yet, but these can be considered in the future.

This work was created as a pet project and a way to practice Python (https://docs.python.org/3/library/) and Gmail Client Libraries API (e.g. https://developers.google.com/gmail/api/v1/reference/users/labels) Actual code was much imported from the Gmail API Examples provided. The initial code actually started from this tutorial: https://developers.google.com/sheets/api/quickstart/python

# How to run 
```
your-prompt$ python manage-gmail-labels.py
usage: manage-gmail.labels.py [-h] [-v] [-l] [-c COUNT] [-a ADD] [-rm REMOVE] [-ren RENAME RENAME]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l, --list            list all labels
  -c COUNT, --count COUNT
                        counts how many message have been assigned a specific
                        label
  -a ADD, --add ADD     add a label
  -rm REMOVE, --remove REMOVE
                        remove an existing label
  -ren RENAME RENAME, --rename RENAME RENAME
                        rename a label
```
