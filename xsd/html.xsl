<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" version="2.0">
	<xsl:template match="/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl">
	<xsl:variable name="latestDate">
	<!-- gets latest date -->
          <xsl:for-each select="//entry">
            <xsl:sort select="@dateTime" order="descending" />
            <xsl:if test="position() = 1">
              <xsl:value-of select="@dateTime"/>
            </xsl:if>
          </xsl:for-each>
	</xsl:variable>
		<html>
		<head>
		<title>Reports, last:<xsl:value-of select="$latestDate" /></title>
		</head>
		<body>
		<h1 id="top">System reports of <xsl:value-of select="/report/systemInfo/@name" /></h1>
    <!-- TOC: -->
    <xsl:for-each select="//entry">
      <!-- newest first -->
      <xsl:sort select="position()" data-type="number" order="descending"/>
      <a href="#{@id}" >
      Report of <xsl:value-of select="@dateTime"/>
      </a><br />
    </xsl:for-each >
		<hr/>
		
		<xsl:for-each select="//entry">
      <!-- newest first -->
      <xsl:sort select="position()" data-type="number" order="descending"/>
			<h1 id="{@id}">
					Report of <xsl:value-of select="@dateTime"/>
				</h1>
				
<pre><xsl:for-each select="hdUsage" >HD Usage:     <xsl:value-of select="@current" /> / <xsl:value-of select="@total"/> =&gt; <xsl:value-of select="round(@current div @total * 100)"/>%<br />
</xsl:for-each>
<xsl:for-each select="memUsage"     >Memory Usage: <xsl:value-of select="@current"/> / <xsl:value-of select="@total"/> =&gt; <xsl:value-of select="round(@current div @total * 100)"/>%
</xsl:for-each >Processes:    <xsl:value-of select="processCount" /><br />

<!-- show the other items -->
<xsl:for-each select="other"> 
<xsl:for-each select="*">
<!-- print the name -->
<!-- if they contain text, print that, if they have attributes, show those -->
<xsl:value-of select="name()"/>: <xsl:choose>
<xsl:when test="string-length(.) &gt; 0">
<xsl:value-of select="."/>
</xsl:when >
<xsl:otherwise >
<xsl:for-each select="@*">
<xsl:value-of select="name()"/> = <xsl:value-of select="."/>
</xsl:for-each>
</xsl:otherwise >
</xsl:choose>
<br />
</xsl:for-each>
</xsl:for-each>
				</pre>
        <a href="#top">&#8593; back to top</a>
        <br />
        <br />
		</xsl:for-each>
<style>
pre, code, kbd, samp { font-family: monospace, serif; _font-family: 'courier new', monospace; font-size: 1em; }
pre { white-space: pre; white-space: pre-wrap; word-wrap: break-word; }
html, button, input, select, textarea { font-family: sans-serif; color: #222; }
body { margin: 1em; font-size: 1em; line-height: 1.4; }
a {text-decoration: none; }
</style>
    
    
		</body>
		</html>
    </xsl:template>
    
<xsl:template match="@*">
<xsl:value-of select="name()"/> = <xsl:value-of select="."/><br/>
</xsl:template>
</xsl:stylesheet>