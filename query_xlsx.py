#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import string
import jieba
import jieba.analyse
import operator
from read_xlsx import get_file_names


DATA_PATH = './dist2/'

PAGE_NAME = 'Unnamed: 1'
PAGE_CONTENT = 'Unnamed: 7'
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

SHOW_MAX = 30

def query():
    xlsx_file_names = get_file_names(DATA_PATH)
    my_dict = {}
    counter = 0
    counter_n = 0
    # Dict init.
    for k in QUERY_KEYWORD:
        my_dict[k] = []
    for n in xlsx_file_names:
        counter_n += 1
        try:
#            print "[*] Reading ", "*" * 10, n, "*" * 10
            xl_file = pd.ExcelFile(DATA_PATH + n)
            page = xl_file.parse('Timeline')
            counter += len(page[PAGE_NAME].real)
            if len(page[PAGE_NAME].real) != len(page[PAGE_CONTENT].real):
                print len(page[PAGE_NAME].real), " != ", len(page[PAGE_CONTENT].real)
            for p, c in zip(page[PAGE_NAME].real, page[PAGE_CONTENT].real):
                for k in QUERY_KEYWORD:
                    try:
                        c_encode = c.encode('utf-8')
                        if k in p.encode('utf-8') or k in c_encode:
                            my_dict[k].append(filterpunt(c_encode))
#                            my_dict[k].append((p, c))
                    except:
                        pass
        except:
            print "[*] Error in file ", n
            print sys.exc_info()
            continue
    print 'counter ', counter
    print 'counter_n ', counter_n
    return my_dict

def term_frequency():
    d = query()
    k_num = {}
    for k in QUERY_KEYWORD:
        d_for_k = {}
        content = d[k]
        k_num[k] = len(content)
        for c in content:
            #c_cut = jieba.cut(c, cut_all=False)
            c_cut = jieba.analyse.extract_tags(c, topK=len(c)/5)
            try:
                list_c = list(c_cut)
            except:
                pass
            for char in list_c:
                if char not in d_for_k:
                    d_for_k[char] = 1
                else:
                    d_for_k[char] += 1
        d[k] = d_for_k

    for k in QUERY_KEYWORD:
        sorted_d_k = sorted(d[k].items(), key=operator.itemgetter(1))
        sorted_d_k.reverse()
        counter = 0
        print k, " # of contents: ", k_num[k]
        for _ in sorted_d_k:
            print sorted_d_k[counter][0], ": ", sorted_d_k[counter][1]
            counter += 1
            if counter > SHOW_MAX:
                break
        print "*" * 10

if __name__ == "__main__":
    term_frequency()
