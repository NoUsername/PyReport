'''
Created on 26.02.2012

@author: Paul Klingelhuber - s1010455@students.fh-hagenberg.at
'''

import sys, os
import Config
import Util

if __name__ == '__main__':
    # check if all necessary libs are here:
    
    allGood = True
    
    try:
        from lxml import etree #@UnusedImport
    except ImportError:
        print("lxml library not installed, please get it from here: http://lxml.de")
        allGood = False
    
    try:
        import psutil #@UnusedImport
    except ImportError:
        print("psutil library not installed, please get it from here: http://code.google.com/p/psutil/")
        allGood = False
        
    if not allGood:
        print("exiting now")
        exit()
    
    thisFilesPath = os.path.realpath(__file__)
    thisFilesDir = os.path.abspath(os.path.join(thisFilesPath, os.path.pardir))
    Util.MAIN_FOLDER = thisFilesDir
    os.chdir(Util.MAIN_FOLDER)
    
    print("Starting...")
    successfully = False
    
    try:
        from Reporter import Reporter
        r = Reporter()
        if not r.load():
            raise Exception("could not load document")
        
        if r.appendNewEntry():
            r.checkAlarms()
            if r.save():
                successfully = True
                if not Config.RSS_AND_HTML_BASE_URL:
                    print("RSS_AND_HTML_BASE_URL not configured in Config.py\nWon't do conversion to rss or html")
                else:
                    from Transformer import Transformer
                    urlbase = Config.RSS_AND_HTML_BASE_URL
                    if not urlbase.endswith("/"):
                        urlbase = urlbase + "/"
                    x = Transformer(copyToDir=Config.COPY_RSS_AND_HTML_HERE)
                    x.makeTransformations(baseURL=urlbase)
        else:
            print("error while appending new entry!")
    except:
        print("error:")
        import traceback
        print(sys.exc_info()[0])
        print(traceback.format_exc())
    print("Finished "+(successfully and "successfully" or "with errors"))
    
    
    # end
