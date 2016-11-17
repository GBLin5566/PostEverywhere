#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import sys
from read_xlsx import get_file_names

DATA_PATH = './data/dist2/'

PAGE_NAME = 'Unnamed: 1'
PAGE_CONTENT = 'Unnamed: 7'
QUERY_KEYWORD = ['統一', '統一AB', '福樂', '林鳳營', '光泉']


def query():
    xlsx_file_names = get_file_names(DATA_PATH)
    my_dict = {}
    # Dict init.
    for k in QUERY_KEYWORD:
        my_dict[k] = []
    for n in xlsx_file_names:
        try:
            print "[*] Reading ", "*" * 10, n, "*" * 10
            xl_file = pd.ExcelFile(DATA_PATH + n)
            page = xl_file.parse('Timeline')
            for p, c in zip(page[PAGE_NAME].real, page[PAGE_CONTENT].real):
                for k in QUERY_KEYWORD:
                    try:
                        if k in p.encode('utf-8') or k in c.encode('utf-8'):
                            my_dict[k].append((p, c))
                            print "Append ", k
                            print "With ", p, " says ", c
                    except:
                        pass
        except:
            print "[*] Error in file ", n
            print sys.exc_info()
            continue

    return my_dict

if __name__ == "__main__":
    d = query()
    for k in QUERY_KEYWORD:
        print k
        print len(d[k])
