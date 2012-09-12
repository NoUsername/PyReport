PyReport Guide
==============

*by Paul Klingelhuber - [paul@paukl.at](mailto:paul@paukl.at)*


Installation
------------

This description assumes you already have Python 2.7 installed.

How to install the additional dependencies:

**Windows**

Go to [http://code.google.com/p/psutil/downloads/list](http://code.google.com/p/psutil/downloads/list "http://code.google.com/p/psutil/downloads/list")
download & install psutil-x.x.x.win32-py2.7.exe

	easy_install --allow-hosts=lxml.de,*.python.org lxml==2.2.2



**Ubuntu** (or similar Linux distributions e.g. Debian)

*Only necessary if errors occur (no full python installation available)*

	sudo apt-get install python2.7-dev
	sudo apt-get install python-pip
	sudo apt-get install libxml2-dev

*And one of the following two -> try the second one if the first one fails:*

	sudo apt-get install libxslt-dev
	sudo apt-get install libxslt1-dev

*This will probably always be necessary*

	sudo pip install psutil
	sudo pip install lxml


Config
------

Open the file `PyReport/Config.py` and change configure as you need, the settings are documented directly in the file and here for reference:

	# - FOLDERS SETUP - 
	## you can use your own simply by replacing it with sth like:
	# COPY_RSS_AND_HTML_HERE = "C:/apache/htdocs/reporter/"
	## or on Linux:
	# COPY_RSS_AND_HTML_HERE = "/var/www/reporter/"
	## lastly specify the base url for the links inside the html report
	# RSS_AND_HTML_BASE_URL = "http://www.yourserver.com/reporter/"
	# You could also use the Dropbox Public folder for free hosting
	
	COPY_RSS_AND_HTML_HERE = "C:/Users/You/Dropbox/Public/"
	RSS_AND_HTML_BASE_URL = "http://dl.dropbox.com/u/0000000/"

	# - EMAIL SETUP - 
	# for most simple setup, use a gmail address
	# specify the email address and the password below
	# in the basic setup, you will receive an email from yourself
	# when an error occurs
	#  NON-GMAIL: change settings accordingly further below
	ALERT_EMAIL_ENABLED = True
	ALERT_EMAIL_ADDRESS = "yourname@gmail.com"
	ALERT_EMAIL_ADDRESS_PASSWORD = "your_pw"
	

Examples
--------

The generated report HTML will have entries that look like this:

![HTML Report](http://dl.dropbox.com/u/1526874/PyReport/site/html.png)

Furthermore, it generates an RSS feed which can be consumed via any RSS reader, for example the online [Google Reader](http://www.google.at/reader "Google Reader") but also via email clients such as Thunderbird.
When configured correctly, a click on an item from an RSS feed will take you to the HTML report document at the correct position.

Here you see the report being displayed in Google Reader:<br/>
![Report displayed in Google Reader](http://dl.dropbox.com/u/1526874/PyReport/site/reader.png)

The image also shows a custom reporter, which displays the number of `WebDavAccounts` existing on this server, which is simply the folder count in a specific directory.

This shows a screenshot of Thunderbird displaying a feed with formatting which has a link to the HTML file in a public Dropbox folder:<br/>
![Report displayed in Thunderbird](http://dl.dropbox.com/u/1526874/PyReport/site/thunderbird.png)

XML
---

All data from PyReport is held in XML files. They can be found in:

	PyReport/xml/

The most central file is `reports.xml`, it holds all the results of all reporting runs that have been done.
If there was ever an error in this file, it will be backed up, so if you see files like `reports.xml.1337343583.96.bak` in there, it is a backup of an old version which was no longer readable by PyReport. This can happen when validation against the schema definition fails.
If you look at the file, maybe you can find something that could have caused this (e.g. an uncareful manual edit).

The directoy also contains the transformation results to the RSS feed `feed.xml` and the transformation result to the HTML report `items.html`.
If you specified a directory in the config variable `COPY_RSS_AND_HTML_HERE` these two files will also show up in the specified folder.

Another important directory is:

	PyReport/xsd/

It contains our report data schema `report.xsd`, which defines how a valid `reports.xml` file must look like. Furthermore it contains `html.xsd` which is our transformation from a `reports.xml` to the HTML report file and `rss.xsl` which is our transformation to the RSS feed file.

The RSS feed file looks a little more confusing, because for formatting in RSS you need to put the encoded HTML tags, so instead of having `<br />` like in the HTML transformation we need to write `&lt;br /&gt;` .
Apart from that, the two transformations are similar.

The HTML report also contains an index of all the contained reports at the beginning as you saw in the screenshot at the beginning of the Examples section.

If you want to custimize any of the transformations simply edit these files, but this should only be done if you really know XSLT!



Have it your way!
-----------------

It is extremely easy to create such custom reporters and can be a very powerful tool when you tailor it to your needs.
All you need to do is toss in new reporter scripts in:

	PyReporter/reporters/

Simply have a look at the tiny scripts that are already in there and you will instantly get how to use it.
This is a fully functional example which returns a random number which will be displayed as the room temperature:

	import random
	
	def doTest():
	    return ("roomTemperature", str(random.randint(15, 25)))

Here is a more useful example, which checks the number of elements in the temporary directory:

	import os
	
	def doTest():
	    return ("itemsInTempDir", len(os.listdir(os.environ['TEMP'])))

And don't be afraid from experimenting! You can't do anything wrong, even if exceptions are triggered, PyReporter will catch them and continue with the other reports. So the worst thing that can happen is that your custom report is missing.

So go for it! Experiment!

Oh and did i mention the same goes for alarms? Just check out this folder:

	PyReport/alarms/

Writing an alarm trigger is as easy as:

	CHECK_FOR = "processCount"
	
	def doCheck(oldVal, newVal):   
	    if newVal > 100:
	        return "High process count, currently %d processes."%newVal

As you see in the method parameters, you olso get the old value (from the previous run). And since your reporters can return multiple values as dictionaries, you can work on these values here too as seen in this example:

	CHECK_FOR = "memUsage"
	# memUsage values consist of 2 items "current" and "total"
	
	def doCheck(oldVal, newVal):
	    # always check if oldVal is None (e.g. first run
		#                        or didn't exist before)!
	    if oldVal is None:
	        oldVal = newVal
	    
	    # we get: current and total, we only need current
	    oldVal = oldVal["current"]
	    newVal = newVal["current"]
	    
	    if newVal > 2*oldVal:
	        return "Memory consumption has at least doubled!"

Again, for the alarm triggers it is also safe to experiment, when an alarm trigger produces an error, it will be caught and the rest of the triggers/reporters and all the good stuff simply continues!

<br />
*PyReport &#169; 2012 by Paul Klingelhuber*