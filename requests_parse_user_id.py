#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import lib.
import sys
import os
import time
import requests
import random
import json
from bs4 import BeautifulSoup
from read_xlsx import get_file_names
import codecs

JSON_DIR = "./crawler_data/json/"
WRITE_JSON_DIR = "./crawler_data/json_new/"
PROFILE_URL_PREFIX = "https://www.facebook.com/profile.php?id="

def main():

    json_files = get_file_names(JSON_DIR, '.json')
    
    for json_file in json_files:
        print "Accessing ", json_file
        try:
            with open(JSON_DIR + json_file, 'r') as f:
                datas = json.load(f)
            for k in range(len(datas)):
                try:
                    if "info" in datas[k]:
                        if "comments" in datas[k]["info"]:
                            for i, c in enumerate(datas[k]["info"]["comments"]):
                                try:
                                    user_url = c["url"]
                                    new_url = find_user_id_from_url(user_url)
                                    if new_url:
                                        datas[k]["info"]["comments"][i]["url"] = new_url
                                except:
                                    print "[*] Writing comment url exception: ",sys.exc_info()
                                    continue
                        if "likes" in datas[k]["info"]:
                            for i, l in enumerate(datas[k]["info"]["likes"]):
                                try:
                                    user_url = l
                                    new_url = find_user_id_from_url(user_url)
                                    if new_url:
                                        datas[k]["info"]["likes"][i] = new_url
                                except:
                                    print "[*] Writing like url exception: ",sys.exc_info()
                                    continue
                        if "shares" in datas[k]["info"]:
                            for i, s in enumerate(datas[k]["info"]["shares"]):
                                try:
                                    user_url = s["url"]
                                    new_url = find_user_id_from_url(user_url)
                                    if new_url:
                                        datas[k]["info"]["shares"][i]["url"] = new_url
                                except:
                                    print "[*] Writing share url exception: ",sys.exc_info()
                                    continue
                except:
                    print "[*] Writing data exception: ",sys.exc_info()[0]
            print "Writing file ", WRITE_JSON_DIR + json_file
            with codecs.open(WRITE_JSON_DIR + json_file, "w+", encoding="utf-8") as outfile:
                json.dump(datas, outfile, indent=4, ensure_ascii=False)
        except:
            print "[*] Read file exception: ",sys.exc_info()[0]
            print "[*] Escaping ", json_file
            continue

def find_user_id_from_url(url):
    new_url = ""
    try:
        time.sleep(random.randint(3,5))
        res = requests.get(url)
        print "Requests get [ ", url, " ] success."
    except KeyboardInterrupt:
        sys.exit(-1)
    except:
        print "[*] Get url exception: ",sys.exc_info()[0]
        return new_url

    content = res.content
    id_content = parse_user_id(content)
    if not id_content:
        return new_url
    new_url = PROFILE_URL_PREFIX + id_content
    return new_url

def parse_user_id(content):
    entity_id_start = content.find("entity_id")
    if entity_id_start == -1:
        return ""
    entity_id_end = content[entity_id_start:].find("\"") + entity_id_start
    id_start = content[entity_id_end+1:].find("\"") + entity_id_end + 2
    id_end = content[id_start:].find("\"") + id_start
    return content[id_start:id_end]

if __name__ == "__main__":
    main()
