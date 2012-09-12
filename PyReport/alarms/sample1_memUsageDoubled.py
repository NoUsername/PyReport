'''
Created on Apr 2, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

## this example operates on the memory usage
CHECK_FOR = "memUsage"

def doCheck(oldVal, newVal):
    '''
    it's good practice to always check if oldVal is None
      if oldVal is None:
        oldVal = newVal
    is one pattern that you can use
    '''
    
    # always check if oldVal is None (e.g. first run, or didn't exist before)!
    if oldVal is None:
        oldVal = newVal
    
    # we get current and total values, we only need current here
    oldVal = oldVal["current"]
    newVal = newVal["current"]
    
    if newVal > 2*oldVal:
        return "Memory consumption has at least doubled!"
    
    # if there is nothing wrong with the value, simply don't return anything!
    