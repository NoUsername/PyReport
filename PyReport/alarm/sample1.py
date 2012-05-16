'''
Created on Apr 2, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

CHECK_FOR = "memUsage"

def doCheck(oldVal, newVal):
    # always check if oldVal is None (e.g. first run, or didn't exist before)!
    if oldVal is None:
        oldVal = newVal
    
    if newVal > 2*oldVal:
        return "OH NO, MEMORY CONSUMPTION DOUBLED!"
    
    # if there is nothing wrong with the value, simply don't return anything!
    