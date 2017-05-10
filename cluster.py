# -*- coding: utf-8 -*-
import os
import math


def Dot(dic1, dic2):
    """Calculate inner product between 2 vectors of 2 texts"""
    fin = 0
    for i in dic1:
        if i in dic2:
            fin += dic1[i] * dic2[i]
    return fin


def Cos(dic1, dic2):
    fin = Dot(dic1, dic2) / math.sqrt(Dot(dic1, dic1) * Dot(dic2, dic2))
    # print(fin)
    return fin


def Cos2(dic1, dic2):
    fin = 0
    for i in dic1:
        if i in dic2:
            fin += 1
    tot = math.sqrt(len(dic1, dic2))
    return fin / tot


def Getfa(fa, i):
    if fa[i] == i:
        return i
    fa[i] = Getfa(fa, fa[i])
    return fa[i]


def Cluster(vectors, tvalue, typ=0):
    tot = len(vectors)

    # use for sorting
    sor = []                                     # used for sort
    matx = []
    for i in range(tot):
        matx.append([])
    for i in range(tot):
        for j in range(i + 1, tot):
            # print(i, j)
            if typ:
                cosval = Cos2(vectors[i], vectors[j])
            else:
                cosval = Cos(vectors[i], vectors[j])
            sor.append((i, j, cosval))
            matx[j].append(cosval)

    sor = sorted(sor, key=lambda x: x[2], reverse=True)

    fa = []
    for i in range(tot):
        fa.append(i)

    for t in sor:
        # print(t[2])
        if t[2] < tvalue:
            break
        # print(t[2])
        Getfa(fa, t[0])
        Getfa(fa, t[1])
        if fa[t[0]] != fa[t[1]]:
            # print(t[0], t[1])
            fa[fa[t[0]]] = fa[t[1]]

    for i in range(tot):
        Getfa(fa, i)

    fin1 = []
    fin = []
    for i in range(tot):
        fin1.append([])
    for i in range(tot):
        fin1[fa[i]].append(i)
    for i in fin1:
        if i:
            fin.append(i)

    for i in range(tot):
        matx[i].append(1.0)
    for i in range(tot):
        for j in range(i + 1, tot):
            matx[i].append(matx[j][i])
    # print(matx)

    return fin, matx


def Try():
    v = [{'a': 1, 'b': 1, 'c': 1}, {'x': 1, 'y': 1}, {'x': 1, 'z': 1}]
    fin = Cluster(v, 0.4)
    print(fin)

if __name__ == '__main__':
    Try()
