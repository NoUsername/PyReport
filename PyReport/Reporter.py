'''
Created on 29.02.2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import os, sys, time
from XmlTester import XmlTester
from EntryCreator import EntryCreator
from lxml import objectify
from lxml import etree
from Alarms import Alarms
import Util

class Reporter(object):
    '''
    Reporter class handles the reports.xml file.
    It reads it and writes new values to it.
    
    '''

    def __init__(self, path="../xml/reports.xml"):
        '''
        Constructor
        a path for the report files can be specified, if not, the default path is used
        '''
        self.doc = None
        self.path = Util.GETPATH(path)
        self.pathDir = os.path.split(self.path)[0]
        if not os.path.exists(self.pathDir):
            os.makedirs(self.pathDir)        
        
    def createDefaultDoc(self):
        E = objectify.ElementMaker(annotate=False) #@UndefinedVariable
        root = E.report(E.systemInfo)
        
        return etree.ElementTree(root)
        
    def load(self):
        x = XmlTester(Util.GETPATH("../xsd"))
        ok = False
        if (os.path.exists(self.path)):
            ok, doc, errors = x.checkIsReports(self.path) #@UnusedVariable
            if not ok:
                print("old file is invalid! " + str(errors))
        if ok:
            self.doc = objectify.parse(self.path) #@UndefinedVariable
        else:
            print("recreating new file")
            if (os.path.exists(self.path)):
                os.rename(self.path, "%s.%s.bak"%(self.path, str(time.time())))
            self.doc = self.createDefaultDoc()
            ok = True

        return ok
    
    def appendNewEntry(self):
        c = EntryCreator()
        c.create()
        root = self.doc.getroot()
        if root is not None:
            root.append(c.reportXml)
            #print(etree.tostring(self.doc, pretty_print=True))
            return True
        else:
            print("no root found!")
            return False
        
    def checkAlarms(self):
        root = self.doc.getroot()
        xmlValsOld = None
        if len(root.getchildren()) > 2:
            xmlValsOld = root.getchildren()[-2]
        xmlValsNew = root.getchildren()[-1]
        
        oldValues = self.getValuesFromXml(xmlValsOld)
        newValues = self.getValuesFromXml(xmlValsNew)
        
        checker = Alarms(oldValues, newValues)
        checker.checkForAlarms()
        
    def getValuesFromXml(self, node):
        if node is None:
            return None
        #print(node)
        entries = node.getchildren()
        result = {}
        otherItems = None
        for item in entries:
            if (item.tag == "other"):
                otherItems = item
            else:
                result[item.tag] = self.parseNode(item)
        
        if otherItems is not None:
            entries = otherItems.getchildren()
            for item in entries:
                result[item.tag] = self.parseNode(item)
        
        return result
    
    def parseNode(self, node):
        attribs = node.attrib
        if len(attribs) > 0:
            # create a dictionary with children
            result = {}
            for k, v in attribs.items():
                if v.isdigit():
                    v = int(v)
                result[k] = v
            return result
        else:
            # simply save the nodes content
            if node.text.isdigit():
                return int(node.text)
            return node.text
        
    
    def save(self):
        try:
            f = open(self.path, 'w')
            self.doc.write(f, xml_declaration=True, pretty_print=True)
            f.close()
            return True
        except:
            print("error occurred during save %s"%str(sys.exc_info()))
        

if __name__ == '__main__':
    blub = Reporter()
    if blub.load():
        if blub.appendNewEntry():
            blub.save()
            blub.checkAlarms()
        
        