#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import string
import jieba
import jieba.analyse
import operator
from read_xlsx import get_file_names
import sys

DATA_PATH = './dist2/'

PAGE_NAME = 'Unnamed: 1'
PAGE_LIKE = 'Unnamed: 4'
PAGE_COMMENT = 'Unnamed: 5'
PAGE_SHARE = 'Unnamed: 6'
PAGE_CONTENT = 'Unnamed: 7'

WEIGHT = [1, 1, 1] # Like * [0] + COMMENT * [1] + SHARE * [2]

QUERY_KEYWORD = ['統一', '統一AB', '福樂', '林鳳營', '光泉', '優酪乳']
DICT_PATH = './extra_dict/dict.txt.my.big'
STOPWORDS_PATH = './extra_dict/stop_words.txt'
jieba.load_userdict(DICT_PATH)
jieba.analyse.set_stop_words(STOPWORDS_PATH)
PUNC = set(u'''@#$%^&*()~/:!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
        ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
        々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
        ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
filterpunt = lambda s: ''.join(filter(lambda x: x not in PUNC, s))
filterpuntl = lambda l: list(filter(lambda x: x not in PUNC, l))

SHOW_MAX = 100
DONT_COUNT_OFFICIAL = False
ONLY_OFFICIAL = True

if len(sys.argv) < 2:
    FILE_NAME = 'df_result.txt'
else:
    FILE_NAME = sys.argv[1]

def query():
    xlsx_file_names = get_file_names(DATA_PATH)
    my_dict, my_dict_weight = {}, {}
    counter = 0
    counter_n = 0
    not_in_counter = 0
    # Dict init.
    for k in QUERY_KEYWORD:
        my_dict[k] = []
        my_dict_weight[k] = []
    for n in xlsx_file_names:
        counter_n += 1
        try:
#            print "[*] Reading ", "*" * 10, n, "*" * 10
            xl_file = pd.ExcelFile(DATA_PATH + n)
            page = xl_file.parse('Timeline')
            counter += len(page[PAGE_NAME].real)
            if len(page[PAGE_NAME].real) != len(page[PAGE_CONTENT].real):
                print len(page[PAGE_NAME].real), " != ", len(page[PAGE_CONTENT].real)
            for i, (p, c) in enumerate(zip(page[PAGE_NAME].real, page[PAGE_CONTENT].real)):
                for k in QUERY_KEYWORD:
                    try:
                        c_encode = c.encode('utf-8')
                        if ONLY_OFFICIAL:
                            if k in p.encode('utf-8'):
                                my_dict[k].append(filterpunt(c_encode))
                                like = int(page[PAGE_LIKE].real[i])
                                comment = int(page[PAGE_COMMENT].real[i])
                                share = int(page[PAGE_SHARE].real[i])
                                score = like * WEIGHT[0] + comment * WEIGHT[1] + share * WEIGHT[2]
                                my_dict_weight[k].append(score)
                        elif (not DONT_COUNT_OFFICIAL and (k in p.encode('utf-8') or k in c_encode)) \
                        or (DONT_COUNT_OFFICIAL and k not in p.encode('utf-8') and k in c_encode):
                            my_dict[k].append(filterpunt(c_encode))
                            like = int(page[PAGE_LIKE].real[i])
                            comment = int(page[PAGE_COMMENT].real[i])
                            share = int(page[PAGE_SHARE].real[i])
                            score = like * WEIGHT[0] + comment * WEIGHT[1] + share * WEIGHT[2]
                            my_dict_weight[k].append(score)
                        elif k == "優酪乳":
                            not_in_counter += 1
                    except:
                        pass
        except:
            print "[*] Error in file ", n
            print sys.exc_info()
            continue
    print 'counter ', counter
    print 'counter_n ', counter_n
    print 'not_in_counter ', not_in_counter
    return my_dict, my_dict_weight

def term_frequency():
    d, d_score = query()
    k_num = {}
    for k in QUERY_KEYWORD:
        d_for_k = {}
        content = d[k]
        k_num[k] = len(content)
        for i, c in enumerate(content):
            #c_cut = jieba.cut(c, cut_all=False)
            c_cut = jieba.analyse.extract_tags(c, topK=len(c))
            try:
                list_c = list(c_cut)
            except:
                pass
            for char in list_c:
                if char not in d_for_k:
                    d_for_k[char] = d_score[k][i]
                else:
                    d_for_k[char] += d_score[k][i]
        d[k] = d_for_k
    with open(FILE_NAME, 'w') as f:
        for k in QUERY_KEYWORD:
            sorted_d_k = sorted(d[k].items(), key=operator.itemgetter(1))
            sorted_d_k.reverse()
            counter = 0
            f.write(str(k) + " # of contents: " + str(k_num[k]) + '\n')
            for _ in sorted_d_k:
                f.write(sorted_d_k[counter][0].encode('utf-8') + ": " + str(sorted_d_k[counter][1]) + '\n')
                counter += 1
                if counter > SHOW_MAX:
                    break
            f.write("*" * 10)

if __name__ == "__main__":
    term_frequency()
