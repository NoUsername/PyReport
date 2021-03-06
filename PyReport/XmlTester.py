'''
Created on April 30, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

from lxml import etree
import os
import Util

class XmlTester(object):
    '''
    Can check if an XML file is valid according to an XSD
    '''
    
    def __init__(self,loadXsdFrom="../xsd"):
        '''
        Constructor, you can configure where the xsd files come from
        '''
        #self.alertsXsd = ""
        
        ## checker object for the report xml file
        self.reportsXsd = ""
        
        loadXsdFrom = Util.GETPATH(loadXsdFrom)
        
        #alertsFile = open(os.path.join(loadXsdFrom, "alerts.xsd"))
        #xmlschema_doc = etree.parse(alertsFile)
        #alertsFile.close()
        #self.alertsXsd = etree.XMLSchema(xmlschema_doc)
        
        reportFile = open(os.path.join(loadXsdFrom, "report.xsd"))
        xmlschema_doc = etree.parse(reportFile)
        reportFile.close()
        self.reportsXsd = etree.XMLSchema(xmlschema_doc)
    
#    def checkIsAlerts(self, filename):
#        result = False
#        doc = None
#        try:
#            f = open(filename)
#            doc = etree.parse(f)
#            result = self.alertsXsd.validate(doc)
#            f.close()
#        except:
#            pass
#        return result, doc
    
    def checkIsReports(self, filename):
        '''
        checks if a file, given by filename attribute is a valid
        report XML file
        '''
        result = False
        doc = None
        errors = None
        try:
            f = open(filename)
            doc = etree.parse(f)
            result = self.reportsXsd.validate(doc)
            if not result:
                errors = str(self.reportsXsd.error_log)
            f.close()
        except:
            pass
        return result, doc, errors

#if __name__ == '__main__':
#    c = XmlTester("../xsd/")
#    isRep = c.checkIsReports("test.xml")
#    print(isRep)
#    