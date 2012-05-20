'''
Created on Arpli 10, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import os, sys, time, platform
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
        '''
        creates the default report document structure
        '''
        E = objectify.ElementMaker(annotate=False) #@UndefinedVariable
        root = E.report(E.systemInfo(name=platform.node()) )
        
        return etree.ElementTree(root)
        
    def load(self):
        '''
        loads old reports from xml file
        first checks via XSD if the old file is valid
        if not, it is backed up and a new one is created
        '''
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
        '''
        creates and appends a new entry node
        '''
        c = EntryCreator()
        c.create()
        root = self.doc.getroot()
        if root is not None:
            root.append(c.reportXml)
            return True
        else:
            print("no root found!")
            return False
        
    def checkAlarms(self):
        '''
        runs all the alarm checkers
        first gets the previous and current values in a 
        simple dictionary format to pass to the Alarms class
        '''
        root = self.doc.getroot()
        xmlValsOld = None
        if len(root.getchildren()) > 2:
            xmlValsOld = root.getchildren()[-2]
        xmlValsNew = root.getchildren()[-1]
        
        # first element is the systemInfo node
        systemName = root.getchildren()[0].get("name")
        
        oldValues = self.getValuesFromXml(xmlValsOld)
        newValues = self.getValuesFromXml(xmlValsNew)
        
        checker = Alarms(oldValues, newValues)
        checker.checkForAlarms(systemName)
        
        for alarm in checker.alarms:
            node = etree.SubElement(xmlValsNew.alarms, alarm[0])
            node._setText(alarm[1])
        
    def getValuesFromXml(self, node):
        '''
        reads all the data from an "<entry ... />" node
        '''
        if node is None:
            return None
        #print(node)
        entries = node.getchildren()
        result = {}
        otherItems = None
        for item in entries:
            if (item.tag == "other"):
                otherItems = item
            elif item.tag != 'alarms':
                result[item.tag] = self.parseNode(item)
        
        if otherItems is not None:
            entries = otherItems.getchildren()
            for item in entries:
                result[item.tag] = self.parseNode(item)
        
        return result
    
    def parseNode(self, node):
        '''
        get data from node, either the text (contents)
        or if it has attributes, a dictionary containing the attributes
        if any of this data is a number, it will already be converted to a number
        '''
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
        '''
        saves the current data to the xml file
        '''
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
        
        