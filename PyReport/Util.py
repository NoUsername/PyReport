'''
Created on April 15, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import os
import re

def simpleImport(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def getCleanXmlNodeName(name):
    '''
    gets a name that can safely be used for an xml node-name
    removes spaces, etc
    '''
    rx = re.compile('\W+')
    return rx.sub('_', name).strip()

# this gets configured automaticaly, don't touch!
MAIN_FOLDER = ""

def GETPATH(somepath):
    global MAIN_FOLDER
    """
    somepath may be relative or absolute, if its absolute, it will simply
    be returned
    if it's relative it will be normalized against the start-folder of the app
    so this always returns an absolute path
    """
    if not somepath:
        return somepath
    
    if not MAIN_FOLDER:
        #print("WARNING: MAIN_FOLDER not configured!")
        MAIN_FOLDER = os.getcwd()
    
    if os.path.isabs(somepath):
        return os.path.abspath(somepath)
    else:
        return os.path.abspath(os.path.join(MAIN_FOLDER, somepath))
