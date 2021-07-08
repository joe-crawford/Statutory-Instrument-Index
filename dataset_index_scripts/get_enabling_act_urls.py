#!/usr/bin/env python

# Script to get Enabling Act URLs from Statutory Instrument XML files 
# Download URLs with wget then build index file

import xml.etree.ElementTree as ET
import re

def get_enabling_act(filename):
    xml = ET.parse(filename)

    intro_text = ET.tostring(xml.find('.//{http://www.legislation.gov.uk/namespaces/legislation}SecondaryPreamble' +
        '//{http://www.legislation.gov.uk/namespaces/legislation}Text')).decode('utf-8')

    footnotes = ()
    if match := re.search('FootnoteRef Ref="(\w+)"', intro_text, re.IGNORECASE):
        footnotes = footnotes + match.groups()
        if match := re.search('power.*FootnoteRef Ref="(\w+)"', intro_text, re.IGNORECASE):
            footnotes = match.groups() + footnotes

        citation = xml.find('.//{http://www.legislation.gov.uk/namespaces/legislation}Footnote[@id="' + footnotes[0] +'"]' +
            '//{http://www.legislation.gov.uk/namespaces/legislation}Citation[@Class="UnitedKingdomPublicGeneralAct"]')

        return citation.attrib['URI']

enabling_acts = set()
for line in open('legislation_urls_https.txt'):
    filename = line[8:-1]
    if filename.startswith('www.legislation.gov.uk/uksi'):
        try:
            if act := get_enabling_act(filename):
            enabling_acts.add(act)
    except:
        pass

for act in enabling_acts:
    print(act)

