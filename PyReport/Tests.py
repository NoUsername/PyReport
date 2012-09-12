'''
Created on May 10, 2012

@author: Paul
'''
import unittest

from PyReport import Alarms, Config

class Test(unittest.TestCase):
    '''
    place for automated tests
    '''
    
    def testAlarms(self):
        oldVals = {"hdUsage": {"current": 149, "total": 150}, "memUsage": {"current": 149, "total": 150}, "processCount" : 150}
        x = Alarms.Alarms(oldVals, oldVals)
        Config.ALERT_EMAIL_ENABLED = False
        x.checkForAlarms('testsystem')
        
        self.assertTrue(len(x.alarms) > 0, "alarms should have been found")
        
    
    def testConfig(self):
        import Config
        self.assertTrue(hasattr(Config, "COPY_RSS_AND_HTML_HERE"))
        self.assertTrue(hasattr(Config, "RSS_AND_HTML_BASE_URL"))

    
    def testEntryCreator(self):
        from EntryCreator import EntryCreator
        x = EntryCreator()
        x.create()
        self.assertTrue(("<hdUsage" in x.report and "<memUsage" in x.report), "something is not right with the generated report, it does not contain some required text")
        

if __name__ == "__main__":
    unittest.main()