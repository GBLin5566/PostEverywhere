"""Calculate term freq. for Q search
    Usage: python3 qsearch_statistic.py dist/ [tf_output.txt] [weighted_output.txt]
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import operator
import os
import pandas as pd
import purewords

def get_file_names(data_dir_address, ends_with=".xlsx"):
    """List all the file ends_with keyword.
    Args:
        data_dir_address(str): directory's path.
        ends_with(str): ending keyword.
    Return:
        files(list): list of files' name.
    """
    files = []
    for file in os.listdir(data_dir_address):
        if file.endswith(ends_with):
            files.append(file)
    return files

DATA_PATH = sys.argv[1]
PAGE_NAME = 'Unnamed: 1'
PAGE_LIKE = 'Unnamed: 4'
PAGE_COMMENT = 'Unnamed: 5'
PAGE_SHARE = 'Unnamed: 6'
PAGE_CONTENT = 'Unnamed: 7'
SHOW_MAX = 1000

TF_FILE_NAME = sys.argv[2]
WEIGHTED_TF_FILE_NAME = sys.argv[3]

def query():
    """Sum up the content and content's score
    Returns:
        list_of_contents(list): list contains all the content
                                (content is split by space into list too).
        list_of_contents_score(list): list contains content's score.
    """
    xlsx_file_names = get_file_names(DATA_PATH)
    list_of_contents = []
    list_of_contents_score = []
    for name in xlsx_file_names:
        print("Reading ", name)
        pd_read_xlsx = pd.ExcelFile(DATA_PATH + name)
        pd_page = pd_read_xlsx.parse('Timeline')
        for index, page_content in enumerate(pd_page[PAGE_CONTENT].real):
            try:
                # Preprocess
                if isinstance(page_content, str):
                    list_of_contents.append(purewords.clean_sentence(page_content).split())
                    content_like = int(pd_page[PAGE_LIKE].real[index])
                    content_comment = int(pd_page[PAGE_COMMENT].real[index])
                    content_share = int(pd_page[PAGE_SHARE].real[index])
                    content_score = content_like + content_comment + content_share
                    list_of_contents_score.append(content_score)
            except ValueError:
                # Caused by the non-int value in like/comment/share
                continue
    return list_of_contents, list_of_contents_score

def term_freq():
    """Calculate all terms' freq. and weighted freq.(by LCS), and write out the file."""
    list_of_contents, list_of_contents_score = query()
    tf_dict = {}
    weighted_tf_dict = {}
    for content, score in zip(list_of_contents, list_of_contents_score):
        for char in content:
            if char in tf_dict:
                tf_dict[char] += 1
            else:
                tf_dict[char] = 1
            if char in weighted_tf_dict:
                weighted_tf_dict[char] += score
            else:
                weighted_tf_dict[char] = score

    # Write out
    write_file(TF_FILE_NAME, tf_dict)
    write_file(WEIGHTED_TF_FILE_NAME, weighted_tf_dict)

def write_file(filename, write_dict):
    """Write file for dict.
    Args:
        filename(str): write out file name.
        write_dict(dict): dict to write out.
    """
    with open(filename, "w") as file:
        # Sort
        sorted_write_dict = sorted(write_dict.items(), key=operator.itemgetter(1))
        # Sorted by des.
        sorted_write_dict.reverse()
        for index, _ in enumerate(sorted_write_dict):
            file.write(sorted_write_dict[index][0] + "," + str(sorted_write_dict[index][1]) + "\n")
            if index > SHOW_MAX:
                break

if __name__ == "__main__":
    term_freq()
