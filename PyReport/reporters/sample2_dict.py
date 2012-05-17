'''
Created on 28.02.2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import psutil

def doTest():
    # for more complex measurements, which should contain multiple values,
    # you can return a dictionary
    
    results = psutil.cpu_times()
    
    return ("cpuTimes", {"user" : results[0], "system" : results[1], "idle" : results[2]})