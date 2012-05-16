'''
Created on 26.02.2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

from lxml import etree
from lxml import objectify
import time
import uuid
import SystemTest
import os
import sys
import Util

class EntryCreator(object):
    '''
    creates a report entry
    '''
    
    REPORTER_METHODNAME = "doTest"

    def __init__(self):
        '''
        Constructor
        '''
        self.report = ""
        self.reportXml = None
        
        
    def runDynamicReporters(self):
        lst = os.listdir("./reporters")
        loadme = []
        resDict = {}
        for entry in lst:
            if (entry.endswith(".py") and entry.find("__init__") == -1):
                loadme.append(entry)
        for reporter in loadme:
            try:
                modname = reporter[:-3]
                name = "reporters." + modname
                mod = Util.simpleImport(name)
                functionToCall = getattr(mod, self.REPORTER_METHODNAME)
                result = functionToCall()
                if len(result) != 2:
                    print("ignoring result of `%s` because no 2 element tuple was returned"%modname)
                else:
                    resDict[result[0]] = result[1]
            except:
                print("Unexpected error:" + str(sys.exc_info()))
        return resDict
        
    def create(self):
        E = objectify.ElementMaker(annotate=False) #@UndefinedVariable
        root = E.entry(E.hdUsage, E.memUsage, E.processCount)
        root.set("id", "e_" + str(uuid.uuid4()))
                
        tuple_time = time.gmtime()
        timeStr = time.strftime("%Y-%m-%dT%H:%M:%S", tuple_time)
        root.set("dateTime", timeStr)
        
        hd = SystemTest.getFreeSpace()
        # write used space
        root.hdUsage._setText(str(hd[0] - hd[1]))
        
        procCount = SystemTest.getProcessCount()
        root.processCount._setText(str(procCount))
        
        mem = SystemTest.getMemUsage()
        root.memUsage._setText(str(mem[0]-mem[1]))
        
        resDict = self.runDynamicReporters()
        if (len(resDict) > 0):
            root.other = E.entry()
            for key, val in resDict.items():
                elem = etree.SubElement(root.other, key)
                elem._setText(val)
        
        self.reportXml = root
        self.report = etree.tostring(root, pretty_print=True)
        
        print(self.report)        
        
        
if __name__=='__main__':
    x = EntryCreator()
    x.create()