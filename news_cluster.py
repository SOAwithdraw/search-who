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

    fin = cluster.Cluster(featured_text, 0.3)

    clustered_page = [[url_list[i] for i in c] for c in fin]

    print(json.dumps(clustered_page, ensure_ascii=False))


if __name__ == '__main__':

    filename = 'search.yaml'
    with open(filename) as f:
        all_info = yaml.load(f)

    print(json.dumps(all_info[7]['text'], ensure_ascii=False))
    # cluster_pages(all_info)
