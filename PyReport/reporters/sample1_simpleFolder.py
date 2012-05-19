'''
Created on 28.02.2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import os

def doTest():
    tempDir = os.environ["TEMP"] if "TEMP" in os.environ else "/tmp/"
    return ("itemsInTempDir", len(os.listdir(tempDir)))