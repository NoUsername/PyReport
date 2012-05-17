<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" version="2.0">
    <xsl:param name="baseUrl" />
	<xsl:template match="/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl">
		<rss  version="2.0">
			<channel>
				<title>Reporter Feed of <xsl:value-of select="/report/systemInfo/@name" /></title>
				<link><xsl:value-of select="$baseUrl" /></link>
				<description>system reports</description>
				<pubDate>2012-01-01</pubDate>
				<xsl:for-each select="//entry">
          <!-- newest first -->
          <xsl:sort select="position()" data-type="number" order="descending"/>
					<item>
						<title>
							Report of <xsl:value-of select="@dateTime"/>
						</title>
						<description>
Detailed report:
<xsl:for-each select="hdUsage">HD Usage: <xsl:value-of select="@current" /> / <xsl:value-of select="@total"/> =&gt; <xsl:value-of select="round(@current div @total * 100)"/>% <br/></xsl:for-each>
<xsl:for-each select="memUsage">Memory Usage: <xsl:value-of select="@current"/> / <xsl:value-of select="@total"/> =&gt; <xsl:value-of select="round(@current div @total * 100)"/>%<br/></xsl:for-each>
Processes: <xsl:value-of select="processCount"/><br/>
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

						</description>
						<guid><xsl:value-of select="@id"/></guid>
						<pubDate>
							<xsl:value-of select="@dateTime"/>
						</pubDate>
						<link><xsl:value-of select="$baseUrl" />items.html#<xsl:value-of select="@id"/></link>
					</item>
				</xsl:for-each>
			</channel>
		</rss>
    </xsl:template>
</xsl:stylesheet>
