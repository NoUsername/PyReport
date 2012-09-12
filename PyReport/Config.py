'''
Created on April 10, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''
import os
# CONFIGURE HERE:


## FOLDERS SETUP  \n
## you can use your own simply by replacing it with sth like: \n
#COPY_RSS_AND_HTML_HERE = "C:/apache/htdocs/reporter/" \n
## or on Linux: \n
#COPY_RSS_AND_HTML_HERE = "/var/www/reporter/" \n

COPY_RSS_AND_HTML_HERE = os.path.join(os.getenv('USERPROFILE') or os.getenv('HOME'), "Dropbox/Public/PyReport")
## lastly specify the base url for the links inside the html report \n
##RSS_AND_HTML_BASE_URL = "http://www.yourserver.com/reporter/" \n
## This is an example BASE_URL if you use the Dropbox public folder \n
##RSS_AND_HTML_BASE_URL = "http://dl.dropbox.com/u/0000000/"
RSS_AND_HTML_BASE_URL = "file:///" + COPY_RSS_AND_HTML_HERE.replace("\\", "/") #@UnusedVariable



## EMAIL SETUP \n 
## for most simple setup, use a gmail address  \n
## specify the email address and the password below   \n
## in the basic setup, you will receive an email from yourself   \n
## NON-GMAIL: change settings accordingly further below
ALERT_EMAIL_ENABLED = True
ALERT_EMAIL_ADDRESS = "yourname@gmail.com"
ALERT_EMAIL_ADDRESS_PASSWORD = "your_pw" #@UnusedVariable


# ADVANCED EMAIL SETUP (for non-gmail setup)

## by default, you will get an email from yourself, you could change this here  
ALERT_EMAIL_ADDRESS_FROM = ALERT_EMAIL_ADDRESS

## the server that is used for sending  
EMAIL_SERVER = "smtp.gmail.com:587"
## ssl or not  
EMAIL_USE_TLS = True

## this tries to load a cusotm local config file (ConfigLocal.py)
try:
    from ConfigLocal import * #@UnusedWildImport
    
    if ALERT_EMAIL_ADDRESS_FROM == "yourname@gmail.com":
        ALERT_EMAIL_ADDRESS_FROM = ALERT_EMAIL_ADDRESS
except:
    pass