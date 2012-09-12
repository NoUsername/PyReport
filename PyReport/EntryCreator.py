'''
Created on April 10, 2012

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
    This class is responsible for creating new entries in the report XML
    It is also responsible for discovering and executing custom reporters
    '''
    
    ## name of function which valid reporters must expose
    REPORTER_METHODNAME = "doTest"
    
    ID_CURRENT = "current"
    ID_TOTAL = "total"

    def __init__(self):
        '''
        Constructor
        '''
        ## will contain the new report item serialized to a string
        self.report = ""
        ## will contain the actual new report xml objects 
        self.reportXml = None
        
        
    def __runDynamicReporters(self):
        '''
        this discovers and executes the dynamic reporters
        '''
        lst = os.listdir(Util.GETPATH("./reporters"))
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
                if result is None or len(result) != 2:
                    print("ignoring result of `%s` because no 2 element tuple was returned"%modname)
                else:
                    resDict[result[0]] = result[1]
            except:
                print("Unexpected error:" + str(sys.exc_info()))
        return resDict
        
    def create(self):
        '''
        call this function from external code to execute the generation of the new report values.
        it will set the reportXml and report attributes of this object, where reportXml holds the actual
        xml structure, and report contains this structure serialized to a string
        '''
        E = objectify.ElementMaker(annotate=False) #@UndefinedVariable
        root = E.entry(E.hdUsage, E.memUsage, E.processCount, E.other, E.alarms)
        root.set("id", "e_" + str(uuid.uuid4()))
                
        tuple_time = time.localtime()
        timeStr = time.strftime("%Y-%m-%dT%H:%M:%S", tuple_time)
        root.set("dateTime", timeStr)
        
        hd = SystemTest.getFreeSpace()
        # write used and total space
        root.hdUsage.set(self.ID_CURRENT, str(hd[0] - hd[1]))
        root.hdUsage.set(self.ID_TOTAL, str(hd[0]))
        
        procCount = SystemTest.getProcessCount()
        root.processCount._setText(str(procCount))
        
        mem = SystemTest.getMemUsage()
        # write used and total space
        root.memUsage.set(self.ID_CURRENT, str(mem[0] - mem[1]))
        root.memUsage.set(self.ID_TOTAL, str(mem[0]))
        
        resDict = self.__runDynamicReporters()
        if (len(resDict) > 0):
            #root.other = E.entry()
            for key, val in resDict.items():
                key = Util.getCleanXmlNodeName(key)
                elem = etree.SubElement(root.other, key)
                if type(val) is dict:
                    for k, v in val.items():
                        elem.set(k, str(v))
                else:
                    elem._setText(str(val))
        
        self.reportXml = root
        self.report = etree.tostring(root, pretty_print=True)
        
        #print(self.report)        
        
