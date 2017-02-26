'''

A little helper class for getting the data we care about out of psutil

Created on April 07, 2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import os
import platform
import psutil

def getFreeSpace(path=None):
    """
    returns total, free
    """
    if path==None:
        if platform.system() == 'Windows':
            path = os.environ.get("SystemDrive", "C:\\")
        else:
            path = "/"
    data = psutil.disk_usage(path)
    return data[0], data[2]


def getMemUsage():
    """
    returns total, free
    """
    if hasattr(psutil, 'phymem_usage'):
        data = psutil.phymem_usage()
        return data[0], data[2]
    data = psutil.virtual_memory()
    return data.total, data.free


def getProcessCount():
    """
    returns count of running processes 
    """
    data = psutil.process_iter()
    # data is a generator object, we can't use len() but this does it nicely
    count = sum(1 for dontCare in data) #@UnusedVariable
    return count

def getCpuUsage():
    """
    returns the avg cpu usage in the last 3 seconds
    """
    data = psutil.cpu_percent(3, False)
    return data

def percentOf(total, value):
    return int((float(value)/float(total))*100)

if __name__ == '__main__':
    print(str(getCpuUsage()))
    
    total, free = getFreeSpace()
    print(free, total)
    print(str(percentOf(total, free)) + "%")
    total, free = getMemUsage()
    print(free, total)
    print(str(percentOf(total, free)) + "%")
    
    
    