'''
Created on May 2, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

CHECK_FOR = "hdUsage"

def doCheck(oldVal, newVal):
    # always check if oldVal is None (e.g. first run, or didn't exist before)!
    if oldVal is None:
        oldVal = newVal
    
    # use the "current" value, there is also "max" which gives the total available hd space
    current = newVal["current"]
    old = oldVal["current"]
    if current > 2*old:
        return "OH NO, MEMORY CONSUMPTION DOUBLED!"
    
    # if there is nothing wrong with the value, simply don't return anything!
    