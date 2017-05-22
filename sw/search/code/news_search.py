# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import yaml
import json
import codecs
import sys
import jieba
import jieba.posseg as pseg

import baidunews
import cluster
import photo

reload(sys)
sys.setdefaultencoding("utf-8")
# jieba.enable_parallel()


def nouns_extract(text_list, banned_list, max_length=20):

    def banned(word):
        for banned_word in banned_list:
            if word in banned_word:
                return True
        return False

    nouns_wanted = {'n': 1, 'ns': 2, 'nsf': 3, 'nt': 3, 'nz': 2}  # 名词,地名，音译地名，机构名，其他专名
    all_nouns = {}
    for text in text_list:
        words = pseg.cut(text)
        for w in words:
            if w.flag in nouns_wanted and not banned(w.word) and len(w.word) > 1:
                if w.word not in all_nouns:
                    all_nouns[w.word] = nouns_wanted[w.flag]
                else:
                    all_nouns[w.word] += nouns_wanted[w.flag]

    if len(all_nouns) > 20:
        all_nouns = dict(sorted(all_nouns.items(), key=lambda x: x[1], reverse=True)[:20])

    return all_nouns


def cluster_pages(all_info, th, imggroup, imgs, tp1, tp2, banned_list):
    '''
        传入待聚类的页面信息all_info和一些参数，返回聚类的页面编号
        Args:
            all_info: 页面信息，形式为 [[page1],[page2],...], page = {'text':,'img':,'url':,'id',...}
            th: 聚类阈值，采用层次聚类
            tp1,tp2: 聚类方法，详见cluster.py
            banned_list: 提取特征时禁止的词，一般为搜索的关键字
        Returns:
            clustered_page: 一个list，形式为[[class1_p1,class1_p2,...],[class2_p1,class2_p2,...],...]
            finword: 每一类的关键字
            pictures: 一个list，形式为[class1_pic,class2_pic,...] 
    '''
    info_num = len(all_info)

    url_list = []
    featured_text = []
    for i in range(info_num):
        features = nouns_extract(all_info[i]['text'], banned_list)
        if len(features) > 10:
            url_list.append(i)
            featured_text.append(features)

    fin, finword, pictures = cluster.Cluster(featured_text, th, imggroup, imgs, tp1, tp2)

    clustered_page = [[url_list[i] for i in c] for c in fin]

    return clustered_page, finword, pictures


def cluster_img(all_info):
    """
        图片聚类
        Args:
            all_info: 列表的列表，子列表里面是若干个url
        Returns:
            fin: 列表的列表，子列表里面是若干数字，代表是同一类的标号
            mainphoto: 列表，里面是若干个url
    """
    photos = [x['img'] for x in all_info]
    fin, mainphoto = photo.Cluster(photos)
    return fin, mainphoto


def search(name, describe=[], cache_dir="data"):
    '''
        主要搜索函数，传入名称和其他搜索信息，返回搜索结果
        Args:
            name: 搜索人名
            descrive: 辅助信息，如机构名，地名等等
            cache_dir: 搜索结果保存地址
        Returns:
            search_result: 搜索结果，形式为[(类别关键字，类别图像url，[[url1,title1],[url2,titl2],...]), (类别2), (类别3)...]
    '''
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    print("Search {0} with description {1}".format(name, describe))

    search_word = name if not describe else name + ' ' + ' '.join(describe)
    search_filename = os.path.join(cache_dir, search_word + ".yaml")
    dirname = os.path.join(cache_dir, search_word)
	
    print(search_filename)
    if os.path.exists(search_filename):
        print("Load from cache...")
        with open(search_filename) as f:
            baidu_result = yaml.load(f)
    else:
        print("Start searching news...")
        '''
        baidu_result = baidunews.get(search_word, newscnt=50)
        output = codecs.open(search_filename, "w", "utf-8")
        yaml.dump(baidu_result, default_flow_style=False, stream=output, indent=4, encoding='utf-8', allow_unicode=True, width=1000)
        '''
        result = [['清华大学计算机系', '', [('url11', 'title11'), ('url12', 'title12')]],
                  ['FF14终身优秀玩家', '', [('url21', 'title21'), ('url22', 'title22')]],
                  ['资深睡眠大师', '', [('url31', 'title31'), ('url32', 'title32')]],
                  ['美食及外卖协会现任董事长', '/static/image/logo.png', [('url41', 'title41'), ('url42', 'title42')]]]

    banned_list = describe
    banned_list.append(name)

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    print(json.dumps(baidu_result, ensure_ascii=False))
    print('Cluster by images.')
    fin, mainphoto = cluster_img(baidu_result)
    print(mainphoto)

    th, tp1, tp2 = 0.15, 0, 1
    print('Cluster by texts.')
<<<<<<< HEAD
    pages, finword, pictures= cluster_pages(baidu_result, th, fin, mainphoto, tp1, tp2, banned_list)
    print(pages)
    print(finword)
    print(pictures)
=======
    pages, finword, pictures = cluster_pages(baidu_result, th, fin, mainphoto, tp1, tp2, banned_list)
>>>>>>> cdd9c37bb10d3a32ab062137c7e61fbe9350b3ad

    search_result = []
    for i in range(len(pages)):
        class_info = []
        for page in pages[i]:
            class_info.append([baidu_result[page]['url'], baidu_result[page]['title']])
        search_result.append([finword[i], pictures[i], class_info])

    # for Debug
    print(pages)
    print(json.dumps(finword, ensure_ascii=False))

    # for i in range(len(pages)):
    #     with codecs.open(dirname + '/' + str(i) + '.txt', 'w', 'utf-8') as fout:
    #         for j in range(len(pages[i])):
    #             fout.write('[' + str(pages[i][j]) + ']\n')
    #             fout.write('\n'.join(baidu_result[pages[i][j]]['text']))
    #             fout.write(json.dumps(featured_text[fin[i][j]], ensure_ascii=False))
    #             fout.write('\n')
    #             fout.write('\n===========\n')

    return search_result


if __name__ == '__main__':
    search("唐杰")
