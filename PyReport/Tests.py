'''
Created on May 10, 2012

@author: Paul
'''
import unittest

from PyReport import Alarms, Config

class Test(unittest.TestCase):
    
    def testAlarms(self):
        oldVals = {"hdUsage": {"current": 149, "total": 150}, "memUsage": {"current": 149, "total": 150}, "processCount" : 150}
        x = Alarms.Alarms(oldVals, oldVals)
        Config.ALERT_EMAIL_ENABLED = False
        x.checkForAlarms()
        
        self.assertTrue(len(x.alarms) > 0, "alarms should have been found")
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()