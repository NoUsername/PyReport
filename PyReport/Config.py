'''
Created on Mar 3, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''
import os
# CONFIGURE HERE:

# - FOLDERS SETUP - 
## you can use your own simply by replacing it with sth like:
# COPY_RSS_AND_HTML_HERE = "C:/apache/htdocs/reporter/"
## or on Linux:
# COPY_RSS_AND_HTML_HERE = "/var/www/reporter/"
## lastly specify the base url for the links inside the html report
# RSS_AND_HTML_BASE_URL = "http://www.yourserver.com/reporter/"
## This is an example BASE_URL if you use the Dropbox public folder
# RSS_AND_HTML_BASE_URL = "http://dl.dropbox.com/u/0000000/"

COPY_RSS_AND_HTML_HERE = os.path.join(os.getenv('USERPROFILE') or os.getenv('HOME'), "Dropbox/Public/PyReport")
RSS_AND_HTML_BASE_URL = "file:///" + COPY_RSS_AND_HTML_HERE.replace("\\", "/")


# - EMAIL SETUP - 
# for most simple setup, use a gmail address
# specify the email address and the password below
# in the basic setup, you will receive an email from yourself
#  NON-GMAIL: change settings accordingly further below
ALERT_EMAIL_ENABLED = True
ALERT_EMAIL_ADDRESS = "yourname@gmail.com"
ALERT_EMAIL_ADDRESS_PASSWORD = "your_pw"



# ANDVANCED EMAIL SETUP (for non-gmail setup)

ALERT_EMAIL_ADDRESS_FROM = ALERT_EMAIL_ADDRESS

EMAIL_SERVER = "smtp.gmail.com:587"
EMAIL_USE_TLS = True
