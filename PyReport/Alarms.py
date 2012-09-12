'''
Created on Apr 2, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import os
import Util
import sys
import traceback
from SimpleMailer import SimpleMailer
import Config

class Alarms(object):
    '''
    The Alarms class is responsible for discovering and running the alarm trigger checkers
    contains the alarm checking code
    '''
    
    ## this is the name of the variable which alarm trigger checkers have to include \n
    ## e.g.: \n
    ##    CHECK_FOR = "cpuTimes"  \n
    ## this has to be at the root level of an alarm trigger file
    ALARM_CHECKFORNAME = "CHECK_FOR"
    
    ## the function name for the checking function \n
    ## e.g.: 
    ALARM_METHODNAME = "doCheck"


    def __init__(self, oldValues=None, newValues=None):
        '''
        Constructor
        oldData map of old values
        newData map of new values
        keys are what was checked (node names in xml)
        values are the actual values
        '''
        if oldValues is None:
            oldValues = {}
        if newValues is None:
            newValues = {}
        
        ## a dictionary of all the old values
        self.oldValues = oldValues
        ## dictionary of all the new (current) values
        self.newValues = newValues
        ## all alarms that were triggered
        self.alarms = []
        
    def __runAlarmCheckers(self):
        '''
        Runs all the alarm checker scripts found in the alarm folder.
        The scripts must define a variable called CHECK_FOR which holds the
        name of which item to check against
        additionally a function that is called doCheck(p1, p2) and receives two
        parameters, the first one will hold the value from a previous reporting
        run (if there was any) and the second will hold the current value
        if the function returns nothing (or None) it means no alarm is triggered
        when it returns something, the string version of it will be inserted in the
        alarm log
        '''
        lst = os.listdir(Util.GETPATH("./alarms"))
        loadme = []
        resDict = {}
        for entry in lst:
            if (entry.endswith(".py") and entry.find("__init__") == -1):
                loadme.append(entry)
        for reporter in loadme:
            try:
                modname = reporter[:-3]
                name = "alarms." + modname
                mod = Util.simpleImport(name)
                checkForAttr = getattr(mod, self.ALARM_CHECKFORNAME)
                
                oldVal = self.oldValues.get(checkForAttr, None)
                newVal = self.newValues.get(checkForAttr, None)
                
                if newVal is not None:
                    functionToCall = getattr(mod, self.ALARM_METHODNAME)
                    result = functionToCall(oldVal, newVal)
                    if (result is not None):
                        print("alarm for %s, alarm msg: %s"%(checkForAttr,result))
                        self.alarms.append([checkForAttr, str(result)])
                else:
                    print("ERROR: we don't have any value for '%s', won't check"%checkForAttr)
                    
            except:
                print("Unexpected error:" + str(sys.exc_info()))
                print(traceback.format_exc())
        return resDict
    
    def __reportAlarms(self, systemName):
        '''
        if there are alarms, this will trigger the mail sending
        '''
        if len(self.alarms) < 1:
            return
        
        msg = '\n'.join(self.messagesOnly())
        title = 'ALARMS of ' + systemName
        msg = title + '\n' + msg
        if Config.ALERT_EMAIL_ENABLED:
            SimpleMailer().send(title, msg)
        
    
    def messagesOnly(self):
        for item in self.alarms:
            yield item[1]
        
    
    def checkForAlarms(self, systemName):
        '''
        call this from external code to trigger the alarm checking
        '''
        self.__runAlarmCheckers()
        try:
            self.__reportAlarms(systemName)
        except:
            print("Error reporting the alarms:" + str(sys.exc_info()))
            print(traceback.format_exc())
        
        