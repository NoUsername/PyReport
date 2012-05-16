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
		<h1 id="top">Infos:</h1>
		<hr/>
		
		<xsl:for-each select="//entry">
			<h1 id="{@id}">
					Report of <xsl:value-of select="@dateTime"/>
				</h1>
				<pre>
					Detailed report:
					HD Usage:     <xsl:value-of select="hdUsage"/><br/>
					Memory Usage: <xsl:value-of select="memUsage"/><br/>
					Processes:    <xsl:value-of select="processCount"/><br/>
				</pre>
				<a href="#top">GO TO TOP</a>
		</xsl:for-each>
		</body>
		</html>
    </xsl:template>
</xsl:stylesheet>