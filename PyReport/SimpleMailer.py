'''
Created on May 10, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''
import smtplib
from email.mime.text import MIMEText
import Config

class SimpleMailer(object):
    '''
    simple interface for sending emails via smtp
    '''

    def __init__(self):
        '''
        Constructor
        currently does nothing
        '''
        pass
        
    def send(self, subject="", content="test content"):
        '''
        send an email with a given subject and content from/to the email address configured
        in the Config file
        '''
        if (Config.ALERT_EMAIL_ADDRESS == 'yourname@gmail.com'):
            print("ERROR: Won't send email notifications until you configure it! "+
            "Go to Config.py for this.")
            return False
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['To'] = Config.ALERT_EMAIL_ADDRESS
        
        server = smtplib.SMTP(Config.EMAIL_SERVER)
        server.ehlo()
        if Config.EMAIL_USE_TLS:
            server.starttls()
        server.ehlo()
        server.login(Config.ALERT_EMAIL_ADDRESS_FROM, Config.ALERT_EMAIL_ADDRESS_PASSWORD)
        
        try:
            server.sendmail(Config.ALERT_EMAIL_ADDRESS_FROM, Config.ALERT_EMAIL_ADDRESS, msg.as_string())
        except:
            print("an error occured while sending mail!")
            return False
        server.quit()
        return True
        