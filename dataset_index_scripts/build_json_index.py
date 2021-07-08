#!/usr/bin/env python

# Script to build JSON index of SIs by Enabling Act

import xml.etree.ElementTree as ET
import re
import json

def get_filenames(urls_filename):
    with open(urls_filename) as urls_file:
        return [url[8:] for url in urls_file.read().splitlines()]

# UK SIs only
uksi_filenames = [fname for fname in get_filenames('si_urls.txt') if fname.startswith('www.legislation.gov.uk/uksi')]

# UK PGAs
ukpga_filenames = get_filenames('acts_urls.txt')

def get_footnotes(xml):
    intro_text = ET.tostring(xml.find('.//{http://www.legislation.gov.uk/namespaces/legislation}SecondaryPreamble' +
        '//{http://www.legislation.gov.uk/namespaces/legislation}Text')).decode('utf-8')
    footnotes = ()
    if match := re.search('FootnoteRef Ref="(\w+)"', intro_text, re.IGNORECASE):
        footnotes = footnotes + match.groups()
        if match := re.search('power.*FootnoteRef Ref="(\w+)"', intro_text, re.IGNORECASE):
            footnotes = match.groups() + footnotes
    return footnotes

def get_enabling_act_uri(xml):
    for footnote in get_footnotes(xml):
        citation = xml.find('.//{http://www.legislation.gov.uk/namespaces/legislation}Footnote[@id="' + footnote +'"]' +
            '//{http://www.legislation.gov.uk/namespaces/legislation}Citation[@Class="UnitedKingdomPublicGeneralAct"]')
        if citation is not None and 'URI' in citation.attrib:
            return citation.attrib['URI']

def get_filename_from_uri(uri):
    return uri[7:] + "/data.xml"

def get_uri_index(uri, acts):
    for i in range(len(acts)):
        if acts[i]["uri"] == uri.replace("/id", "") + "/contents":
            return i

def get_legislation(filename):
    try:
        xml = ET.parse(filename)
        uri = xml.find('.//{http://purl.org/dc/elements/1.1/}identifier').text
        title = xml.find('.//{http://purl.org/dc/elements/1.1/}title').text
        year = int(xml.find('.//{http://www.legislation.gov.uk/namespaces/metadata}Year').attrib['Value'])
        number = int(xml.find('.//{http://www.legislation.gov.uk/namespaces/metadata}Number').attrib['Value'])
        type_ = xml.find('.//{http://www.legislation.gov.uk/namespaces/metadata}DocumentMainType').attrib['Value']
        if type_ == "UnitedKingdomPublicGeneralAct":
            return { "uri": uri, "title": title, "year": year, "number": number, "uksis": [] }
        elif type_ == "UnitedKingdomStatutoryInstrument":
            return { "uri": uri, "title": title, "year": year, "number": number }
    except Exception as e:
        print(filename, e)


uksis = [uksi for filename in uksi_filenames if (uksi := get_legislation(filename))]
ukpgas = [ukpga for filename in ukpga_filenames if (ukpga := get_legislation(filename))]

for si in uksis:
    filename = get_filename_from_uri(si["uri"])
    try:
        xml = ET.parse(filename)
        pga = get_enabling_act_uri(xml)
        if pga:
            #print("pga", pga, "uksi", si["uri"])
            ukpgas[get_uri_index(pga, ukpgas)]["uksis"].append(si)
    except Exception as e:
        print(filename, e)

with open('index.json', 'w', encoding='utf-8') as output:
    json.dump(ukpgas, output, ensure_ascii=False, indent=4)
