# Grocery_List:
Automate Google Drive Document Analysis.
# Description:
This program was designed to interact with google drive to determine if a
current list stored there is out of date and whether it requires additional
objects. After analysis this program makes use of Twilio and the smtplib to 
send text and email notifications respectively.

# Installation:
This porgram requires that a few dependancies be downloaded before operation.
These downloads are made using pip. If pip is not installed on your machine 
run get-pip.py for in this directory.

After pip has been verified or installed run setup.py.

# Script settings:
To control notifications, contacts to which notificaitons are sent, file used, 
and debugging settings open settings.json.Some of these conditions can also be
controled through cmd line args. To see these entries type Main.py -h in the 
terminal.

# Common Goods:
In order to view, add, or remove items on the current common goods list you 
must run commonItemManager.py

# Fuctionality:
Many of the scripts in this directory can be run individualy for testing but for
full program functionality run Main.py with your desired command line arguments. 
