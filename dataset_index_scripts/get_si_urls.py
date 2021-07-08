#!/usr/bin/env python

# Script to get list of SI URLs to download, after scraping data.feed files from legislation website
# Download URLs with wget then run get_enabling_act_urls.py

import untangle

for i in range(1, 6206):
    xml = untangle.parse(f'data.feed@page={i}')
    for entry in xml.feed.entry:
        for link in entry.link:
            if link["title"] == "XML":
                print(link["href"])

