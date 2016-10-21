#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
# Import selenium Lib.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Chrome binary address
CHROME_DRIVER = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(executable_path=CHROME_DRIVER)

# Let's pretend we have url already
POST_URL = ["https://www.facebook.com/daan4fanyun/posts/1393449957351633",
            "https://www.facebook.com/HypeSphere/posts/1265387123502758",
            "https://www.facebook.com/HypeSphere/posts/1265388413502629"]

LIKE_LIST_CLASSNAME = "_1g5v" # Pretty dirty way ...
SHARE_LIST_CLASSNAME = "_4bl9"
LIKE_LIST_USER_CLASSNAME = "_5i_q"
CLICK_LIMIT = 3


for url in POST_URL:
    # Try to get the page
    try:
        driver.get(url)
        while True:
            try:
                driver.find_element_by_id('loginbutton')
                print "[*] Should Log-in"
                import time
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
                time.sleep(1)
    except:
        print "[*] Show more user exception: ",sys.exc_info()[0]
    # Get user id & url
    try:
        user_list = driver.find_elements_by_class_name(LIKE_LIST_USER_CLASSNAME)
        print "Like number: ", len(user_list)
        for u in user_list:
            try:
                single_user = u.find_element_by_css_selector("a")
                print single_user.get_attribute('href')
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
        webdriver.ActionChains(driver).move_to_element(share_link).click(share_link).perform()
        time.sleep(1)
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
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        repost_view_dialog = driver.find_element_by_id('repost_view_dialog')
        share_user = repost_view_dialog.find_elements_by_class_name('userContentWrapper')
        print "Total # of sharing user: ", len(share_user)
        for u in share_user:
            try:
                user_link = u.find_element_by_class_name('fwb').find_element_by_css_selector('a')
                print user_link.text, " ", user_link.get_attribute('href')
                user_content = u.find_element_by_class_name('userContent').find_element_by_css_selector('p').text
                print user_content
            except:
                continue
        # Go to normal page
        webdriver.ActionChains(driver).move_to_element(share_link).click(share_link).perform()
        time.sleep(1)
    except:
        if current_user_count > CLICK_LIMIT:
            break
        current_user_count += 1
        time.sleep(1)

    #################### Share ####################
    
    ####################Comment####################
    # Try to get the post content
    try:
        post_div = driver.find_element_by_class_name('userContentWrapper')
        post_content_div = driver.find_element_by_class_name('userContent')
        post_content_text_list = post_content_div.find_elements_by_css_selector('p')
        post_content_text = ''.join(p.text for p in post_content_text_list)
        print post_content_text
    except:
        print "[*] Get post exception: ",sys.exc_info()[0]
        continue

    # Try to reveall all the hidden comments
    count_reveal = 0
    while True:
        try:
            post_div.find_element_by_class_name('UFILastCommentComponent').find_element_by_class_name('UFIPagerLink').click()
            count_reveal = 0
        except:
            #print "[*] Get hidden comments exception: ",sys.exc_info()[0]
            if count_reveal > CLICK_LIMIT:
                break
            count_reveal += 1
            time.sleep(1)
    # Click all "see more"
    try:
        for see_more in post_div.find_elements_by_css_selector('._5v47.fss'):
            try:
                see_more.click()
            except:
                continue
    except:
        pass

    # Try to go through all the showed comments
    try:
        comment_list = post_div.find_elements_by_class_name('UFICommentContentBlock')
        comment_number = 0
        for comment_block in comment_list:
            '''
            try:
                if comment_block.get_attribute('aria-label') == 'Comment reply'\
                        or comment_block.get_attribute('aria-label') == '回應': # Reply to the comments
                    continue
            except:
                tmp = 0 # Do nothing
            '''
            try:
                user_profile = comment_block.find_element_by_css_selector("a")
                user_profile_url = user_profile.get_attribute('href')
                print "#", comment_number," User ", user_profile.text, " ", user_profile_url
                comment_content = comment_block.find_element_by_class_name("UFICommentBody").text
                print comment_content
                print '-'*10
                comment_number += 1
                if not comment_content:
                    continue
                # Else, save the info
            except:
                continue
        print "Total # of comments: ", comment_number
    except:
        print "[*] Donwload comments exception: ",sys.exc_info()[0]
        #continue
    ####################Comment####################
    

