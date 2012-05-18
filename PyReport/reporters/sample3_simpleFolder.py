'''
Created on 28.02.2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import os

def doTest():
    return ("itemsInTempDir", len(os.listdir(os.environ['TEMP'])))