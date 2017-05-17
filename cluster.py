# -*- coding: utf-8 -*-
import os
from math import log, sqrt

class CosClass:

    def __init__(self , vectors):
        self.vectors = vectors
        self.matx = []
        self.tot = len(vectors)
        for i in range(self.tot):
            self.matx.append([])
        self.idf = {}

    def Clear(self):
        for i in self.matx:
            i = []

    def Getmatx(self):
        return self.matx

    def Getidf(self):
        return self.idf

    def Cos(self, typ):                  # 0: simple neiji  1: bool appearence  2: naive tf-idf  3: inclass tf-idf
        if typ >= 2:
            self.Idf_class()
        else:
            self.Idf()
        for i in range(self.tot):
            for j in range(i + 1, self.tot):
                # print(i, j)
                if typ == 1:
                    cosval = self.Cos1(self.vectors[i], self.vectors[j])
                elif typ >= 2:
                    cosval = self.Cos0(self.vectors[i], self.vectors[j], typ)
                else:
                    cosval = self.Cos0(self.vectors[i], self.vectors[j])
                self.matx[j].append(cosval);

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
                    fin += dic1[i] * dic2[i] * self.idf[i]
                elif typ == 3:
                    fin += log(1 + dic1[i]) * log(1 + dic2[i]) * self.idf[i]
        return fin

    def Cos0(self, dic1, dic2, typ = 0):
        fin = self.Dot(dic1, dic2, typ) / sqrt(self.Dot(dic1, dic1, typ) * self.Dot(dic2, dic2, typ))
        # print(fin)
        return fin

    def Cos1(self, dic1, dic2):
        fin = 0
        for i in dic1:
            if i in dic2:
                fin += 1
        thtot = sqrt(len(dic1) * len(dic2))
        return fin / thtot

    def Idf(self):
        curidf = {}
        for i in self.vectors:
            for j in i:
                cur = curidf.get(j, 0)
                curidf[j] = cur + 1.0
        for i in curidf:
            self.idf[i] = (curidf[i]/self.tot) * (curidf[i]/self.tot)

    def Idf_class(self):
        curidf = {}
        for i in self.vectors:
            for j in i:
                cur = curidf.get(j, 0)
                curidf[j] = cur + 1.0
        for i in curidf:
            curlog = log(self.tot/curidf[i])
            self.idf[i] = curlog * curlog

class CluClass:

    def __init__(self, matx, tvalue):
        self.matx = matx
        self.tot = len(matx)
        self.clu = []
        self.tvalue = tvalue

    def Return(self):
        return self.clu

    def Getfa(self, fa, i):
        if fa[i] == i:
            return i
        fa[i] = self.Getfa(fa, fa[i])
        return fa[i]

    def Clu(self, typ = 1):                        # 0: min clu  1: average clu
        if typ == 0:
            self.Minclu()
        elif typ == 1:
            self.Aveclu()

    def Aveclu(self):
        self.clu = []
        for i in range(self.tot):
            self.clu.append([i])

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

        fa = []

        for i in range(self.tot):
            fa.append(i)

        for t in sor:
            # print(t[2])
            if t[2] < self.tvalue:
                break
            #print(t[2])
            self.Getfa(fa, t[0])
            self.Getfa(fa, t[1])
            if fa[t[0]] != fa[t[1]]:
                # print(t[0], t[1])
                fa[fa[t[0]]] = fa[t[1]]

        for i in range(self.tot):
            self.Getfa(fa, i)

        fin = []
        for i in range(self.tot):
            fin.append([])
        for i in range(self.tot):
            fin[fa[i]].append(i)
        for i in fin:
            if i:
                self.clu.append(i)

def Cluster(vectors, tvalue, typ1, typ2):
    tot = len(vectors)

    # use for sorting
    cosclass = CosClass(vectors)
    cosclass.Cos(typ1)
    matx = cosclass.Getmatx()

    cluclass = CluClass(matx, tvalue)
    cluclass.Clu(typ2)
    fin = cluclass.Return()

    return fin, matx

def Try():
    v = [{'a': 1, 'b': 1, 'c': 1}, {'x': 1, 'y': 1}, {'x': 1, 'z': 1}]
    fin = Cluster(v, 0.4)
    print(fin)

if __name__ == '__main__':
    Try()
