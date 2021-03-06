# -*- coding: utf-8 -*-
import os
import numpy as np
from math import log, sqrt
import json
import pickle


class Person:

    def __init__(self, baike='', weibo='', zhihu='', news=[], picture='', keyword='', index=[], weight=0):
        self.baike = baike
        self.weibo = weibo
        self.zhihu = zhihu
        self.news = news[:]
        self.picture = picture
        self.keyword = keyword
        self.index = index
        self.weight = weight
        self.zhihuinfo = {}

        self.baikes = []
        self.weibos = []
        self.zhihus = []
        self.keywords = []
        self.keywordsweight = 0

    def Calcweight(self):
        self.weight = len(self.news)
        if self.baike != '':
            self.weight += 2
        if self.weibo != '':
            self.weight += 2
        if self.zhihu != '':
            self.weight += 2

    def __str__(self):
        fin = ''
        fin = fin + 'index ' + str(self.index) + '\n'
        fin = fin + 'news ' + '' + str(self.news) + '\n'
        fin = fin + 'baike' + ' ' + str(self.baike) + '\n'
        fin = fin + 'weibo' + ' ' + str(self.weibo) + '\n'
        fin = fin + 'zhihu' + ' ' + str(self.zhihu) + '\n'
        fin = fin + 'zhihuinfo' + ' ' + str(self.zhihuinfo) + '\n'
        fin = fin + 'picture' + ' ' + self.picture + '\n'
        fin = fin + 'keywords ' + str(self.keywords) + '\n'
        fin = fin + 'weight ' + str(self.weight) + '\n'
        return fin

    def Getmainwords(self, vectors, idf):
        fin = []

        for j in idf:
            cur = 0
            for k in self.index:
                cur += vectors[k].get(j, 0)
            cur = cur * 1.0 / len(self.index)

            fin.append({'name': j, 'weight': cur})

        fin = sorted(fin, key=lambda x: x['weight'], reverse=True)
        self.keywords = [x['name'] for x in fin if x['weight'] > 0.9]


class CosClass:

    def __init__(self, vectors):
        self.vectors = vectors
        self.matx = []
        self.tot = len(vectors)
        for i in range(self.tot):
            self.matx.append([])
        self.Idf_class()

    def cutFeature(self):
        new_vectors = []
        for vector in self.vectors:
            tvector = vector
            for word in tvector:
                tvector[word] = tvector[word] * self.idf[word]
            tvector = sorted(tvector.items(), key=lambda x: x[1], reverse=True)[:20]
            new_vector = {}
            for [word, i] in tvector:
                new_vector[word] = vector[word]
            # vector = new_vector
            new_vectors.append(new_vector)
        self.vectors = new_vectors

    def Clear(self):
        for i in self.matx:
            i = []

    def Getmatx(self):
        return self.matx

    def Getidf(self):
        return self.idf

    def Cos(self, typ):                  # 0: simple neiji  1: bool appearence  2: naive tf-idf  3: inclass tf-idf  4: word embedding
        if typ >= 2:
            self.Idf_class()
        # else:
            # self.Idf()
        for i in range(self.tot):
            for j in range(i + 1, self.tot):
                # print(i, j)
                if typ == 1:
                    cosval = self.Cos1(self.vectors[i], self.vectors[j])
                elif typ >= 2:
                    cosval = self.Cos0(self.vectors[i], self.vectors[j], typ)
                else:
                    cosval = self.Cos0(self.vectors[i], self.vectors[j])
                self.matx[j].append(cosval)

        for i in self.matx:
            i.append(1.0)

        for i in range(self.tot):
            for j in range(i + 1, self.tot):
                self.matx[i].append(self.matx[j][i])

    def Dot(self, dic1, dic2, typ):
        """Calculate inner product between 2 vectors of 2 texts"""
        fin = 0
        for i in dic1:
            if i in dic2:
                if typ == 0:
                    fin += dic1[i] * dic2[i]
                elif typ == 2:
                    fin += dic1[i] * dic2[i] * self.idf[i]**2
                elif typ == 3:
                    fin += log(1 + dic1[i]) * log(1 + dic2[i]) * self.idf[i]**2
        return fin

    def Cos0(self, dic1, dic2, typ=0):
        innerproduct = self.Dot(dic1, dic2, typ)
        if innerproduct == 0:
            return 0
        else:
            fin = innerproduct / sqrt(self.Dot(dic1, dic1, typ) * self.Dot(dic2, dic2, typ))
            return fin

    def Cos1(self, dic1, dic2):
        fin = 0
        for i in dic1:
            if i in dic2:
                fin += 1
        thtot = sqrt((len(dic1) + 1) * (len(dic2) + 1))
        return fin / thtot

    # def Idf(self):
    #     curidf = {}
    #     for i in self.vectors:
    #         for j in i:
    #             cur = curidf.get(j, 0)
    #             curidf[j] = cur + 1.0
    #     for i in curidf:
    #         self.idf[i] = (curidf[i] / self.tot) * (curidf[i] / self.tot)

    def Idf_class(self):
        self.idf = {}
        curidf = {}
        for i in self.vectors:
            for j in i:
                cur = curidf.get(j, 0)
                curidf[j] = cur + 1.0
        for i in curidf:
            self.idf[i] = log(self.tot / curidf[i])


class CluClass:

    def __init__(self, matx, tvalue):
        self.matx = matx
        self.tot = len(matx)
        self.clu = [[i] for i in range(self.tot)]
        self.tvalue = tvalue

    def Getfa(self, fa, i):
        if fa[i] == i:
            return i
        fa[i] = self.Getfa(fa, fa[i])
        return fa[i]

    def Imgclu(self, imggroup):
        fa = [i for i in range(self.tot)]

        for i in imggroup:
            host = i[0]
            for j in i:
                if j != host and self.Getfa(fa, j) != self.Getfa(fa, host):
                    fa[fa[j]] = host

        for i in range(self.tot):
            self.Getfa(fa, i)

        fin = []
        self.clu = []
        for i in range(self.tot):
            fin.append([])
        for i in range(self.tot):
            fin[fa[i]].append(i)
        for i in fin:
            if i:
                self.clu.append(i)

    def Return(self):
        return self.clu

    def Clu(self, typ=1):                        # 0: min clu  1: average clu
        if typ == 0:
            self.Minclu()
        elif typ == 1:
            self.Aveclu()

    def Aveclu(self):
        while 1:
            # find closest pair
            ma = 0
            closepair = (0, 0)
            curtot = len(self.clu)
            for i in range(curtot):
                for j in range(i + 1, curtot):
                    sim = 0
                    for ii in self.clu[i]:
                        for jj in self.clu[j]:
                            sim += self.matx[ii][jj]
                    sim /= len(self.clu[i]) * len(self.clu[j])
                    if sim > ma:
                        ma = sim
                        closepair = (i, j)

            if ma < self.tvalue:
                break

            # merge
            i = closepair[0]
            j = closepair[1]
            self.clu[i] = self.clu[i] + self.clu[j]
            del self.clu[j]

    def Minclu(self):
        sor = []
        for i in range(self.tot):
            for j in range(i + 1, self.tot):
                sor.append((i, j, self.matx[i][j]))
        sor = sorted(sor, key=lambda x: x[2], reverse=True)

        fa = [i for i in range(self.tot)]
        for i in self.clu:
            for j in i:
                fa[j] = i[0]

        for t in sor:
            if t[2] < self.tvalue:
                break
            self.Getfa(fa, t[0])
            self.Getfa(fa, t[1])
            if fa[t[0]] != fa[t[1]]:
                fa[fa[t[0]]] = fa[t[1]]

        for i in range(self.tot):
            self.Getfa(fa, i)

        fin = []
        self.clu = []
        for i in range(self.tot):
            fin.append([])
        for i in range(self.tot):
            fin[fa[i]].append(i)
        for i in fin:
            if i:
                self.clu.append(i)


def Fitbest(infos, group, matx, info_type):
    """
    To find the best baike/zhihu of the user if he has more than one url in the list
    Args:
        infos: 
        vectors: the vectors generated by cosclass
        info_type: 'baike' or 'zhihu' or 'weibo'
    Returns:
        the url
    """
    maw = -1
    indw = -1
    for i in group:
        if infos[i]['type'] == info_type:
            curw = 0
            for j in range(len(infos)):
                if i != j:
                    curw += matx[i][j]
            if curw > maw:
                maw = curw
                indw = i

    if indw == -1:
        return ''

    return infos[indw]['url']


def Getmainword(group, vectors, idf):
    fin = []
    for i in group:
        ma = 0
        mainword = ''
        for j in idf:
            cur = 0
            for k in i:
                cur += vectors[k].get(j, 0)
            if cur > ma:
                ma = cur
                mainword = j
        fin.append(mainword)
    return fin


def Getpictures(group, imggroup, imgs):
    fin = []
    for i in group:
        ma = 0
        cur = -1
        for j in range(len(imggroup)):
            inters = len([k for k in i if k in imggroup[j]])
            if inters > ma:
                ma = inters
                cur = j
        if cur > -1:
            fin.append(imgs[cur])
        else:
            fin.append('')
    return fin


def Organize(infos, vectors, groups, keywords, pictures, matx):
    print(groups)
    tot = len(groups)
    persons = []
    for i in range(tot):
        persons.append(Person())
        for j in groups[i]:
            if infos[j]['type'] == 'news':
                persons[i].news.append({'url': infos[j]['url']})
            elif infos[j]['type'] == 'baike':
                persons[i].baikes.append(infos[j]['url'])
            elif infos[j]['type'] == 'weibo':
                persons[i].weibos.append(infos[j]['url'])
            elif infos[j]['type'] == 'zhihu':
                persons[i].zhihus.append(infos[j]['url'])
        persons[i].index = groups[i]
        persons[i].picture = pictures[i]
        persons[i].keyword = keywords[i]
        persons[i].baike = Fitbest(infos, groups[i], matx, 'baike')
        persons[i].zhihu = Fitbest(infos, groups[i], matx, 'zhihu')
        persons[i].weibo = Fitbest(infos, groups[i], matx, 'weibo')
        persons[i].Calcweight()

    return persons


def Pickle(infos, imggroup, imgs):
    f = open('pickle.txt', 'wb')
    pickle.dump(infos, f)
    pickle.dump(imggroup, f)
    pickle.dump(imgs, f)
    f.close()


def Cluster(infos, tvalue, imggroup, imgs, typ1=0, typ2=1):
    """
    main function
    Args:
        infos: [{'type':'news' , 'url':'', 'text':{'x':1}}]
        imggroup: [[1, 2],[3, 4, 1]]
        imgs: ['http.jpg', 'http.png']
    Return:
        fin: [Person, Person]
        """
    #Pickle(infos, imggroup, imgs)
    print("Cluster ", imggroup, tvalue)

    vectors = []
    for i in infos:
        vectors.append(i['text'])
    tot = len(vectors)

    # use for sorting
    cosclass = CosClass(vectors)
    cosclass.Cos(typ1)
    matx = cosclass.Getmatx()

    cluclass = CluClass(matx, tvalue)
    cluclass.Imgclu(imggroup)                     # use img infomation to cluster
    cluclass.Clu(typ2)
    groups = cluclass.Return()
    # groups = [x for x in groups if len(x)>1]

    finword = Getmainword(groups, vectors, cosclass.Getidf())
    pictures = Getpictures(groups, imggroup, imgs)
    persons = Organize(infos, vectors, groups, finword, pictures, matx)

    persons = sorted(persons, key=lambda x: x.weight, reverse=True)
    for i in persons:
        i.Getmainwords(vectors, cosclass.Getidf())
    return persons


def Try():
    v = [{'type': 'baike', 'url': '1', 'text': {'a': 1, 'b': 1, 'c': 1}},
         {'type': 'zhihu', 'url': '2', 'text': {'y': 1, 'x': 1}},
         {'type': 'weibo', 'url': '3', 'text': {'w': 1, 'x': 1}},
         {'type': 'zhihu', 'url': '4', 'text': {'f': 1, 'g': 1}},
         {'type': 'weibo', 'url': '5', 'text': {'h': 1, 'g': 1}}]
    imggroup = [[0, 1], [0, 1]]
    imgs = ['img1', 'img2']
    persons = Cluster(v, 0.1, imggroup, imgs, 0, 1)
    for i in persons:
        print i


def Trypickle():
    f = open('pickle.txt', 'rb')
    infos = pickle.load(f)
    imggroup = pickle.load(f)
    print len(infos)
    imgs = pickle.load(f)
    f.close()
    persons = Cluster(infos, 0.15, imggroup, imgs)
    for i in persons:
        print i

if __name__ == '__main__':
    Trypickle()
