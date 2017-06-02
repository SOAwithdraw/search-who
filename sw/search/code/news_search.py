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
import baike
import zhihuuser

reload(sys)
sys.setdefaultencoding("utf-8")
# jieba.enable_parallel()


def nouns_extract(text_list, banned_list, max_length=20):

    def banned(word):
        for banned_word in banned_list:
            if word in banned_word or word == u'中国':
                return True
        return False

    nouns_wanted = {'n': 1, 'ns': 4, 'nsf': 4, 'nt': 3, 'nz': 2}  # 名词,地名，音译地名，机构名，其他专名
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

    cityname=[]
    for i in all_nouns:
        if i[-1] == u'市' or i[-1] == u'省' or i[-1] == u'县':
            cityname.append(i)
    for i in cityname:
        val = all_nouns[i]
        del all_nouns[i]
        all_nouns[i[:-1]] = val

    return all_nouns

def Order_data(info, info_type, banned_list, feature_len = 1):
    '''
        整理数据，传入某网页数据，输出标准化数据用于聚类
        Args:
            info: yaml data
            info_type: 'baike'/'news'
        Returns:
            fin: ordered data, a list with several dicts
    '''
    fin = []
    for i in info:
        text = ''
        if i.has_key('introdution'):
            text = [i['introdution']]
        elif i.has_key('text'):
            text = i['text']
        elif i.has_key('info'):
            if 'list' in str(type(i['info'])):
                text = i['info']
            else:
                text = [i['info']]

        #text = json.dumps(text).encode('utf-8')
        #print(text)
        features = nouns_extract(text, banned_list)
        
        if len(features) > feature_len:
            fin.append({})
            fin[-1]['url'] = i.get('url', '')
            fin[-1]['text'] = features
            fin[-1]['type'] = info_type

    print("ordered data: " + info_type +  ' ' + str(len(fin)))
    return fin

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


def cluster_img(baidu_info, baike_info, zhihu_info, weibo_info):
    """
        图片聚类
        Args:
            all_info: 列表的列表，子列表里面是若干个url
        Returns:
            fin: 列表的列表，子列表里面是若干数字，代表是同一类的标号
            mainphoto: 列表，里面是若干个url
    """
    photos = [x['img'] for x in baidu_info]
    baike_photos = [[] for x in baike_info]
    zhihu_photos = [[x['img']] for x in zhihu_info]
    weibo_photos = [[x['img']] for x in weibo_info]
    photos.extend(baike_photos)
    photos.extend(zhihu_photos)
    photos.extend(weibo_photos)

    groups, mainphoto = photo.Cluster(photos)
    return groups, mainphoto


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
    #search_filename = os.path.join(cache_dir, "search1.yaml")
    baike_filename = os.path.join(cache_dir, search_word + "baike.yaml")
    print(baike_filename)
    zhihu_filename = os.path.join(cache_dir, search_word + "zhihu.yaml")
    weibo_filename = os.path.join(cache_dir, "weibo3.yaml")
    dirname = os.path.join(cache_dir, search_word)
	
    print(search_filename)
    if os.path.exists(search_filename):
        print("Load from cache...")
        with open(search_filename) as f:
            baidu_result = yaml.load(f)
    else:
        print("Start searching news...")
        baidu_result = baidunews.get(search_word, newscnt=50)
        output = codecs.open(search_filename, "w", "utf-8")
        yaml.dump(baidu_result, default_flow_style=False, stream=output, indent=4, encoding='utf-8', allow_unicode=True, width=1000)
        #result = [['清华大学计算机系', '', [('url11', 'title11'), ('url12', 'title12')]],
         #         ['FF14终身优秀玩家', '', [('url21', 'title21'), ('url22', 'title22')]],
          #        ['资深睡眠大师', '', [('url31', 'title31'), ('url32', 'title32')]],
           #       ['美食及外卖协会现任董事长', '/static/image/logo.png', [('url41', 'title41'), ('url42', 'title42')]]]

    if os.path.exists(baike_filename):
        print("Load baike from cache...")
        with open(baike_filename) as baike_f:
            baike_result = yaml.load(baike_f)
    else:
        print("Start searching baike...")
        baike_result = baike.getpeople(search_word)
        output = codecs.open(baike_filename, "w", "utf-8")
        yaml.dump(baike_result, default_flow_style=False, stream=output, indent=4, encoding='utf-8', allow_unicode=True, width=1000)

    if os.path.exists(zhihu_filename):
        print("Load zhihu from cache...")
        with open(zhihu_filename) as zhihu_f:
            zhihu_result = yaml.load(zhihu_f)
    else:
        print("Start searching zhihu...")
        zhihu_result = zhihuuser.getuser(search_word)
        output = codecs.open(zhihu_filename, "w", "utf-8")
        yaml.dump(zhihu_result, default_flow_style=False, stream=output, indent=4, encoding='utf-8', allow_unicode=True, width=1000)

    banned_list = describe
    banned_list.append(name)

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    #这里添加了几句测试用的社交帐号的语句
    with open(weibo_filename) as weibo_f:
        weibo_result = yaml.load(weibo_f)
    ordered_data = Order_data(baidu_result, 'news', banned_list, 10)
    ordered_data.extend( Order_data(baike_result, 'baike', banned_list))
    ordered_data.extend( Order_data(zhihu_result, 'zhihu', banned_list))
    ordered_data.extend( Order_data(weibo_result, 'weibo', banned_list))

    #print(json.dumps(baidu_result, ensure_ascii=False))
    print('Cluster by images.')
    #imggroup, mainphoto = cluster_img(baidu_result, baike_result, zhihu_result, weibo_result)
    #print(mainphoto)

    th, tp1, tp2 = 0.1, 0, 1
    print('Cluster by texts.')

    persons = cluster.Cluster(ordered_data, th, [], [], tp1, tp2)

    for i in persons:
        print(i)
    """search_result = []
    for i in range(len(persons)):
        class_info = []
        for page in persons[i].news:
            class_info.append([baidu_result[page]['url'], baidu_result[page]['title']])
        search_result.append([finword[i], pictures[i], class_info])"""

    # for Debug
    #print(pages)
    #print(json.dumps(finword, ensure_ascii=False))

    # for i in range(len(pages)):
    #     with codecs.open(dirname + '/' + str(i) + '.txt', 'w', 'utf-8') as fout:
    #         for j in range(len(pages[i])):
    #             fout.write('[' + str(pages[i][j]) + ']\n')
    #             fout.write('\n'.join(baidu_result[pages[i][j]]['text']))
    #             fout.write(json.dumps(featured_text[fin[i][j]], ensure_ascii=False))
    #             fout.write('\n')
    #             fout.write('\n===========\n')

    return persons


if __name__ == '__main__':
    search("陈驰")
