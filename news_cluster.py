# -*- coding: utf-8 -*-
import os
import cluster
import posseg
import yaml
import json
import codecs
import sys
import numpy as np

reload(sys)
sys.setdefaultencoding("utf-8")


def cluster_pages(all_info, th, tp1, tp2, banned_list):

    info_num = len(all_info)

    url_list = []
    featured_text = []
    for i in range(info_num):
        features = posseg.nouns_extract(all_info[i]['text'], banned_list)
        if len(features) > 5:
            url_list.append(i)
            featured_text.append(features)

    fin, mat = cluster.Cluster(featured_text, th, tp1, tp2)

    clustered_page = [[url_list[i] for i in c] for c in fin]

    return clustered_page, featured_text, fin, mat


def print_page(i, all_info):
    print(json.dumps(all_info[i]['text'], ensure_ascii=False))

if __name__ == '__main__':

    banned_list = ["郭文景"]

    filename = 'search2.yaml'
    with open(filename) as f:
        all_info = yaml.load(f)

    th, tp1, tp2 = 0.6, 0, 0
    pages, featured_text, fin, mat = cluster_pages(all_info, th, tp1, tp2, banned_list)

    print(pages)
    '''for i in range(len(pages)):
        with codecs.open(str(i) + '.txt', 'w', 'utf-8') as fout:
            for j in range(len(pages[i])):
                fout.write('[' + str(fin[i][j]) + ']\n')
                # fout.write('\n'.join(all_info[pages[i][j]]['text']))
                fout.write(json.dumps(featured_text[fin[i][j]], ensure_ascii=False))
                fout.write('\n===========\n')'''

    mat = np.array(mat).astype(np.float)

    while 1:
        inf = raw_input().split()
        i, j = int(inf[0]), int(inf[1])
        print(json.dumps(featured_text[i], ensure_ascii=False))
        print("\n")
        print(json.dumps(featured_text[j], ensure_ascii=False))
        print(mat[i, j])
        print("=======================")
