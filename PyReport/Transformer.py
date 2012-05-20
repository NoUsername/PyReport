'''
Created on April 23, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

from lxml import etree
import os
import shutil
import Util

class Transformer(object):
    '''
    classdocs
    '''

    def __init__(self, loadFrom="../xsd", output="../xml/feed.xml", outputHtml="../xml/items.html", copyToDir=None):
        '''
        Constructor
        '''
        self.targetDir = Util.GETPATH(copyToDir)
        self.targetPath = Util.GETPATH(output)
        self.targetPathHtml = Util.GETPATH(outputHtml)
        self.rssTransform = None
        p = os.path.join(Util.GETPATH(loadFrom), "rss.xsl")
        xslDoc = etree.parse(p)
        self.rssTransform = etree.XSLT(xslDoc)
        
        p = os.path.join(Util.GETPATH(loadFrom), "html.xsl")
        xslDoc = etree.parse(p)
        self.htmlTransform = etree.XSLT(xslDoc)
    
    def makeTransformations(self, fromDoc="../xml/reports.xml", baseURL=""):
        '''
        Transforms the reports xml document into the HTML and RSS files
        '''
        if not baseURL:
            baseURL = "'http://localhost/'"
        else:
            baseURL = "'" + baseURL + "'"
        source = etree.parse(Util.GETPATH(fromDoc))
        result_tree_rss = self.rssTransform(source, baseUrl=baseURL)
        result_tree_html = self.htmlTransform(source)
        
        f = open(self.targetPath, 'w')
        result_tree_rss.write(f, xml_declaration=True, pretty_print=True)
        f.close()
        
        f = open(self.targetPathHtml, 'w')
        result_tree_html.write(f, xml_declaration=True, pretty_print=True)
        f.close()
        
        if self.targetDir != None:
            if not os.path.exists(self.targetDir):
                os.makedirs(self.targetDir)
            fileName = os.path.split(self.targetPath)[1]
            shutil.copy2(self.targetPath, os.path.join(self.targetDir, fileName))
            fileName = os.path.split(self.targetPathHtml)[1]
            shutil.copy2(self.targetPathHtml, os.path.join(self.targetDir, fileName))
    
if __name__ == "__main__":
    dirPath = os.path.join(os.getenv('USERPROFILE') or os.getenv('HOME'), "Dropbox/Public/PyReport")
    x = Transformer(copyToDir=dirPath)
    dropBoxId = "1526874"
    x.makeTransformations(baseURL="http://dl.dropbox.com/u/"+dropBoxId+"/PyReport/")
    