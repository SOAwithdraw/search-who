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


def cluster_pages(all_info):

    info_num = len(all_info)

    url_list = []
    featured_text = []
    for i in range(info_num):
        features = posseg.nouns_extract(all_info[i]['text'])
        if len(features) > 5:
            url_list.append(i)
            featured_text.append(features)

    fin = cluster.Cluster(featured_text, 0.4)

    clustered_page = [[url_list[i] for i in c] for c in fin]

    return clustered_page, featured_text, fin


def print_page(i, all_info):
    print(json.dumps(all_info[i]['text'], ensure_ascii=False))

if __name__ == '__main__':

    filename = 'search2.yaml'
    with open(filename) as f:
        all_info = yaml.load(f)

    pages, featured_text, fin = cluster_pages(all_info)

    for i in range(len(pages)):
        with codecs.open(str(i) + '.txt', 'w', 'utf-8') as fout:
            for j in range(len(pages[i])):
                fout.write('[' + str(pages[i][j]) + ']\n')
                # fout.write('\n'.join(all_info[pages[i][j]]['text']))
                fout.write(json.dumps(featured_text[fin[i][j]], ensure_ascii=False))
                fout.write('\n===========\n')
