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
                                    likes = profile_url_access(user_url)
                                    datas[k]["info"]["comments"][i]["likes"] = likes
                                except:
                                    print "[*] Writing comment data exception: ",sys.exc_info()[0]
                                    continue
                        if "likes" in datas[k]["info"]:
                            new_likes = []
                            for i, l in enumerate(datas[k]["info"]["likes"]):
                                try:
                                    user_url = l
                                    likes_likes = profile_url_access(user_url)
                                    new_likes.append({"url":l, "likes":likes_likes})
                                except:
                                    continue
                            datas[k]["info"]["likes"] = new_likes
                        if "shares" in datas[k]["info"]:
                            for i, s in enumerate(datas[k]["info"]["shares"]):
                                try:
                                    user_url = s["url"]
                                    likes = profile_url_access(user_url)
                                    datas[k]["info"]["shares"][i]["likes"] = likes
                                except:
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


def jsonfile_access(filename):

    PROFILE_LIST = ["https://www.facebook.com/profile.php?id=100000423661008&fref=pb&hc_location=profile_browser",
                    "https://www.facebook.com/gb.lin3"]

    for url in PROFILE_LIST:
        profile_url_access(url)

def profile_url_access(url):
    write_dict = []
    try:
        time.sleep(random.randint(3,10))
        res = requests.get(url)
        print "Requests get [ ", url, " ] success."
    except:
        print "[*] Get url exception: ",sys.exc_info()[0]
        return write_dict
    try:
        soup = BeautifulSoup(res.content, 'html.parser')
    except:
        print "[*] Get soup exception: ",sys.exc_info()[0]
        return write_dict
    try:
        table = soup.find("div", class_ = "phs")
        for tbody in table.find_all("tbody"):
            try:
                label = tbody.find("div", class_ = "labelContainer")
                data = tbody.find("td", class_ = "data")
                a_list = []
                for a in data.find_all("a"):
                    if a['href'] == "#":
                        continue
                    a_list.append({"name":a.text, "like_url":a['href']})
                    #print a.text
                    #print a['href']
                write_dict.append({"type_name":label.text, "links":a_list})
            except:
                print "[*] Get label exception: ",sys.exc_info()[0]
        return write_dict
    except:
        print "[*] Get tbody exception: ",sys.exc_info()[0]
        return write_dict

if __name__ == "__main__":
    main()
