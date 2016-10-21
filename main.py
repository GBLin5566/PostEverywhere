#!/usr/bin/env python
# -*- coding: big5 -*-

import sys
# Import selenium Lib.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Package
from random import random
import time
import json

# My own lib.
from read_xlsx import get_url_from_files 

# Chrome binary address
CHROME_DRIVER = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(executable_path=CHROME_DRIVER)
DATA_DIR_ADDRESS = "./data/dist2/"
JSON_DIR_ADDRESS = "./json/"
'''
# Let's pretend we have url already
POST_URL = ["https://www.facebook.com/daan4fanyun/posts/1393449957351633",
            "https://www.facebook.com/HypeSphere/posts/1265387123502758",
            "https://www.facebook.com/HypeSphere/posts/1265388413502629"]
'''
LIKE_LIST_CLASSNAME = "_1g5v" # Pretty dirty way ...
SHARE_LIST_CLASSNAME = "_4bl9"
LIKE_LIST_USER_CLASSNAME = "_5i_q"
CLICK_LIMIT = 3
'''
Json format
[
    {
        "id": int,
        "page_url": str,
        "page_content": str,
        "likes": [], 
        "shares": [{
                    "url": str,
                    "content": str
        }],
        "comments": [{
                    "url": str,
                    "content": str
        }],
    },
    {
        "id": 1, ...
    }
]

'''
url_dict = get_url_from_files(DATA_DIR_ADDRESS)
finish_file = []


#url_dict = [("333", ["https://www.facebook.com/daan4fanyun/posts/1393449957351633"])]

for F, POST_URL in url_dict:
    json_datas = []
    try:
        for index, url in enumerate(POST_URL):
            # Try to get the page
            json_data = {}
            json_data['info'] = {}
            json_data['info']['page_url'] = url
            try:
	            driver.get(url)
	            while True:
	                try:
	                    driver.find_element_by_id('loginbutton')
	                    print "[*] Should Log-in"
	                    time.sleep(20)
	                except:
	                    break

            except:
	            print "[*] Load page exception: ",sys.exc_info()[0]
	            print "[*] URL: ", url
	            continue
	        
	        # TODO
	        # The comments of the post will not be popped out automatically
	        # Current solution: log-in (and log-in will show more comments automatically )


	        #################### Like ####################
	        # Show like list
            try:
	            a_in_like_block = driver.find_element_by_class_name(LIKE_LIST_CLASSNAME)
	            webdriver.ActionChains(driver).move_to_element(a_in_like_block).click(a_in_like_block).perform()
            except:
	            print "[*] Show like list exception: ",sys.exc_info()[0]
	            continue
	        # Show all the user in "more"
            try:
	            count_like_list = 0
	            total_number = 0
	            pre_total_number = 0
	            pre_pre_total_number = 0
	            while True:
	                try:
	                    driver.find_element_by_id('reaction_profile_pager').find_element_by_class_name('uiMorePagerPrimary').click()
	                    if total_number == len(driver.find_elements_by_class_name(LIKE_LIST_USER_CLASSNAME)) == pre_total_number == pre_pre_total_number:
	                        break
	                    pre_pre_total_number = pre_total_number
	                    pre_total_number = total_number
	                    total_number = len(driver.find_elements_by_class_name(LIKE_LIST_USER_CLASSNAME))
	                    count_like_list = 0
	                except:
	                    if count_like_list > CLICK_LIMIT:
	                        break
	                    count_like_list += 1
	                    time.sleep(random()*2+1)
            except:
	            print "[*] Show more user exception: ",sys.exc_info()[0]
	        # Get user id & url
            json_data['info']['likes'] = []
            try:
	            user_list = driver.find_elements_by_class_name(LIKE_LIST_USER_CLASSNAME)
	            print "Total # of like number: ", len(user_list)
	            for u in user_list:
	                try:
	                    single_user = u.find_element_by_css_selector("a")
	                    json_data['info']['likes'].append(single_user.get_attribute('href'))
	                except:
	                    print "[*] Like list user exception: ",sys.exc_info()[0]
	                    continue
            except:
	            "[*] Go through like list exception: ",sys.exc_info()[0]
	        #################### Like ####################
	        
	        #################### Share ####################
	        # Show share list
            try:
                post_div = driver.find_element_by_class_name('userContentWrapper')
                share_link = post_div.find_element_by_class_name('UFIShareLink')
                close_click = driver.find_element_by_css_selector('._42ft._5upp._50zy.layerCancel._1f6._51-t._50-0._50z-')
                webdriver.ActionChains(driver).move_to_element(close_click).click(close_click).perform()
                time.sleep(random()+1)
                webdriver.ActionChains(driver).move_to_element(share_link).click(share_link).perform()

            except:
	            print "[*] Share list exception: ",sys.exc_info()[0]
	            continue

	        # Show all user
            try:
                current_user_count = 0
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random()*4)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                repost_view_dialog = driver.find_element_by_id('repost_view_dialog')
                share_user = repost_view_dialog.find_elements_by_class_name('userContentWrapper')
                print "Total # of sharing user: ", len(share_user)
                json_data['info']['shares'] = []
                for u in share_user:
                    share_dict = {}
                    try:
                        user_link = u.find_element_by_class_name('fwb').find_element_by_css_selector('a')
                        share_dict['url'] = user_link.get_attribute('href')
                    except:
                        share_dict['url'] = ""
                        pass
                    try:
                        user_content = u.find_element_by_class_name('userContent').find_element_by_css_selector('p').text
                        share_dict['content'] = user_content.replace('\n', ' ')
                    except:
                        share_dict['content'] = ""
                        pass
                    json_data['info']['shares'].append(share_dict)

            except:
	            if current_user_count > CLICK_LIMIT:
	                break
	            current_user_count += 1
	            time.sleep(random()*2)


	        #################### Share ####################
	        
	        ####################Comment####################
	        # Try to get the post content
            try:
                # Go to normal page
                close_click = driver.find_element_by_css_selector('._42ft._5upp._50zy.layerCancel._51-t._50-0._50z-')
                webdriver.ActionChains(driver).move_to_element(close_click).click(close_click).perform()
                time.sleep(3)
                post_div = driver.find_element_by_class_name('userContentWrapper')
                post_content_div = driver.find_element_by_class_name('userContent')
                post_content_text_list = post_content_div.find_elements_by_css_selector('p')
                post_content_text = ''.join(p.text for p in post_content_text_list)
                json_data['info'] ['page_content'] = post_content_text
#                print post_content_text
            except:
	            print "[*] Get post exception: ",sys.exc_info()[0]
	            continue

	        # Try to reveall all the hidden comments
            count_reveal = 0
            comment_block_number = 0
            pre_comment_block_number = 0
            while True:
                try:
	                post_div.find_element_by_class_name('UFILastCommentComponent').find_element_by_class_name('UFIPagerLink').click()
	                if comment_block_number == len(post_div.find_elements_by_class_name('UFICommentContentBlock')) == pre_comment_block_number:
	                    break
	                pre_comment_block_number = comment_block_number
	                comment_block_number = post_div.find_elements_by_class_name('UFICommentContentBlock')
	                count_reveal = 0
                except:
	                #print "[*] Get hidden comments exception: ",sys.exc_info()[0]
	                if count_reveal > CLICK_LIMIT:
	                    break
	                count_reveal += 1
	                time.sleep(random()*2)
	        '''
            # Click all "see more"
            try:
                for see_more in post_div.find_elements_by_css_selector('._5v47.fss'):
                    try:
                        webdriver.ActionChains(driver).move_to_element(see_more).click(see_more).perform()
                    except:
	                    continue
            except:
	            pass
            '''
	        # Try to go through all the showed comments
            json_data['info']['comments'] = []
            try:
                comment_list = post_div.find_elements_by_class_name('UFICommentContentBlock')
                comment_number = 0
                for comment_block in comment_list:
                    try:
                        more = comment_block.find_elements_by_css_selector('._5v47.fss')
                        driver.execute_script("return arguments[0].scrollIntoView();", more)
                        more.click()
                    except:
                        pass
                    try:
                        comment_dict = {}
                        user_profile = comment_block.find_element_by_css_selector("a")
                        user_profile_url = user_profile.get_attribute('href')
#                        print "#", comment_number," User ", user_profile.text, " ", user_profile_url
                        comment_content = comment_block.find_element_by_class_name("UFICommentBody").text
#                        print comment_content
#                        print '-'*10
                        comment_dict['url'] = user_profile_url
                        comment_dict['content'] = comment_content.replace('\n', ' ')
                        comment_number += 1
                        if not comment_content:
	                        continue
	                    # Else, save the info
                        json_data['info']['comments'].append(comment_dict)
                    except:
	                    continue
                print "Total # of comments: ", comment_number
            except:
	            print "[*] Donwload comments exception: ",sys.exc_info()[0]
	            #continue
	        ####################Comment####################
            finish_file.append(F)
            json_data['_id'] = index
            json_datas.append(json_data)
            time.sleep(random()*10)
    except:
        print "Last file ", F
        import cPickle
        cPickle.dumpt(finish_file, "finish_file.pkl")
    import codecs
    with codecs.open(JSON_DIR_ADDRESS + F+".json", "w+", encoding="utf-8") as outfile:
        json.dump(json_datas, outfile, indent=4, ensure_ascii=False)
