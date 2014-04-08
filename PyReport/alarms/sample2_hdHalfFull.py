'''
Created on May 3, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

CHECK_FOR = "hdUsage"

def doCheck(oldVal, newVal):
    # use the "current" value, there is also "max" which gives the total available hd space
    current = newVal["current"]
    total = newVal["total"]
    if current > total/2:
        percent = long(current/float(max(1,total))*100)
        return "HD is more than half full! (%s%%)"%percent
    
    # if there is nothing wrong with the value, simply don't return anything!
    
