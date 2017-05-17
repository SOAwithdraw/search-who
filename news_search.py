# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import cluster
import posseg
import yaml
import json
import codecs
import sys

import baidunews
import news_cluster

reload(sys)
sys.setdefaultencoding("utf-8")


def search(name, describe=[], cache_dir="data"):

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    print("Search {0} with description {1}".format(name, describe))

    search_word = name if not describe else name + ' ' + ' '.join(describe)
    search_filename = os.path.join(cache_dir, name + ".yaml")
    dirname = os.path.join(cache_dir, name)

    if os.path.exists(search_filename):
        print("Load from cache...")
        with open(search_filename) as f:
            baidu_result = yaml.load(f)
    else:
        print("Start searching news...")
        baidu_result = baidunews.get(search_word)
        output = codecs.open(search_filename, "w", "utf-8")
        yaml.dump(baidu_result, default_flow_style=False, stream=output, indent=4, encoding='utf-8', allow_unicode=True, width=1000)

    banned_list = describe
    banned_list.append(name)

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    th, tp1, tp2 = 0.15, 0, 1
    pages, featured_text, fin, finword = news_cluster.cluster_pages(baidu_result, th, tp1, tp2, banned_list)

    search_result = []
    for i in range(len(pages)):
        class_info = []
        for page in pages[i]:
            class_info.append(['URL', 'TITLE'])
        search_result.append([finword[i], class_info])

    # for Debug
    print(pages)
    print(json.dumps(finword, ensure_ascii=False))

    for i in range(len(pages)):
        with codecs.open(dirname + '/' + str(i) + '.txt', 'w', 'utf-8') as fout:
            for j in range(len(pages[i])):
                fout.write('[' + str(pages[i][j]) + ']\n')
                fout.write('\n'.join(baidu_result[pages[i][j]]['text']))
                fout.write(json.dumps(featured_text[fin[i][j]], ensure_ascii=False))
                fout.write('\n')
                fout.write('\n===========\n')


if __name__ == '__main__':
    search("周正平")
