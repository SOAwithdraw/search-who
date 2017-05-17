# -*- coding: utf-8 -*-
import os
import cluster
import posseg
import yaml
import json
import codecs
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def cluster_pages(all_info, th, tp1, tp2, banned_list):

    info_num = len(all_info)

    url_list = []
    featured_text = []
    for i in range(info_num):
        features = posseg.nouns_extract(all_info[i]['text'], banned_list)
        if len(features) > 10:
            url_list.append(i)
            featured_text.append(features)

    fin, mat, finword = cluster.Cluster(featured_text, th, tp1, tp2)

    clustered_page = [[url_list[i] for i in c] for c in fin]

    return clustered_page, featured_text, fin, finword


def print_page(i, all_info):
    print(json.dumps(all_info[i]['text'], ensure_ascii=False))

if __name__ == '__main__':

    banned_list = ["王逸伦"]

    filename = 'wyl.yaml'
    with open(filename) as f:
        all_info = yaml.load(f)

    # make directory if necessary
    dirname = filename.split('.')[0]
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    th, tp1, tp2 = 0.1, 0, 1
    pages, featured_text = cluster_pages(all_info, th, tp1, tp2, banned_list)

    print(pages)
    print(json.dumps(finword, ensure_ascii=False))
    for i in range(len(pages)):
        with codecs.open(dirname + '/' + str(i) + '.txt', 'w', 'utf-8') as fout:
            for j in range(len(pages[i])):
                fout.write('[' + str(pages[i][j]) + ']\n')
                fout.write('\n'.join(all_info[pages[i][j]]['text']))
                fout.write(json.dumps(featured_text[fin[i][j]], ensure_ascii=False))
                fout.write('\n')
                fout.write('\n===========\n')
