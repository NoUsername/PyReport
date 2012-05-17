'''
Created on May 10, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

CHECK_FOR = "processCount"

def doCheck(oldVal, newVal):   
    if newVal > 100:
        return "High process count, currently %d processes."%newVal
    
    # if there is nothing wrong with the value, simply don't return anything!
    