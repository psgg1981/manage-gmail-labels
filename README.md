# manage-gmail-labels

This is a python command line tool to manage Gmail labels, i.e. creating, deleting, removing. It also keeps track of the performed operations on your Gmail account in a separate .log file. It does not perform any operations over emails as of yet, but these can be considered in the future.

This work was created as a pet project and a way to practice Python (https://docs.python.org/3/library/) and Gmail Client Libraries API (e.g. https://developers.google.com/gmail/api/v1/reference/users/labels) Actual code was much imported from the Gmail API Examples provided. The initial code actually started from this tutorial: https://developers.google.com/sheets/api/quickstart/python

# How to run 
```
your-prompt$ python manage-gmail-labels.py
usage: manage-gmail-labels.py [-h] [-v] [-l] [-c <label>] [-a <new-label>]
                              [-rm <label>]
                              [-ren <existing-label> <new-label-name>]

optional arguments:
  -h, --help                  show this help message and exit
  -v, --version               show program's version number and exit
  -l, --list                  list all labels
  -c <label>, --count <label> counts how many message have been assigned a specific label
  -a <new-label>, --add <new-label>
                              add a label
  -rm <label>, --remove <label>
                              remove an existing label
  -ren <existing-label> <new-label-name>, --rename <existing-label> <new-label-name>
                              rename a label

```
