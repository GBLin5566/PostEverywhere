#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import lib.
import sys
import os
import time
import requests
import random
from bs4 import BeautifulSoup

PROFILE_LIST = ["https://www.facebook.com/profile.php?id=100000423661008&fref=pb&hc_location=profile_browser",
"https://www.facebook.com/gb.lin3"]

for url in PROFILE_LIST:
    try:
        res = requests.get(url)
        print "Requests get [ ", url, " ] success."
    except:
        print "[*] Get url exception: ",sys.exc_info()[0]
        continue
    try:
        soup = BeautifulSoup(res.content, 'html.parser')
    except:
        print "[*] Get soup exception: ",sys.exc_info()[0]
        continue
    try:
        table = soup.find("div", class_ = "phs")
        for tbody in table.find_all("tbody"):
            try:
                label = tbody.find("div", class_ = "labelContainer")
                data = tbody.find("td", class_ = "data")
                for a in data.find_all("a"):
                    if a['href'] == "#":
                        continue
                    print a.text
                    print a['href']
            except:
                print "[*] Get label exception: ",sys.exc_info()[0]

    except:
        print "[*] Get tbody exception: ",sys.exc_info()[0]
        continue
    time.sleep(random.randint(1,3))

