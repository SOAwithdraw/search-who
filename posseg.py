# -*- coding: utf-8 -*-
import jieba
import jieba.posseg as pseg
import sys
import time
import json

reload(sys)
sys.setdefaultencoding("utf-8")

jieba.enable_parallel()


def nouns_extract(text_list, banned_list):

    nouns_wanted = ['n', 'ns', 'nsf', 'nt', 'nz']
    all_nouns = {}
    for text in text_list:
        words = pseg.cut(text)
        for w in words:
            if w.flag in nouns_wanted and len(w.word) > 1:
                for j in banned_list:
                    if w.word in j:
                        continue
                if w.word not in all_nouns:
                    all_nouns[w.word] = 1
                else:
                    all_nouns[w.word] += 1

    nouns_list = []
    for word, cnt in all_nouns.iteritems():
        nouns_list.append((word, cnt))
    nouns_list = sorted(nouns_list, key=lambda x: x[1], reverse=True)
    if len(nouns_list) > 20:
        nouns_list = nouns_list[:20]

    return dict(nouns_list)


if __name__ == '__main__':
    text = "四川新闻网泸州4月26日讯（赵学龙 )近日，叙永县县委副书记、县长唐杰带领财政局、交通局、水务局、住建局等单位到黄坭乡督导检查安全生产工作，黄坭乡主要领导陪同检查。督查组一行到燕子岩实地察看，详细了解燕子岩事故隐患整改落实情况。唐杰要求：在当前脱贫攻坚的关键时期，一定要进一步提高安全生产认识，强化值班值守和痕迹管理，确保工作措施落实到人，责任落实到位。要加大对安全隐患的排查力度，及时消除隐患。坚持一手抓管理、检查，一手抓宣传教育，做到严格执法。加强对重点行业、重点企业的监督排查，并形成长效机制，对督查时发现的问题要尽快整改。要加强道路交通安全教育宣传，结合实际案例，通过各种安全宣传活动形式，增强大家的安全意识，养成良好的驾驶习惯。"
    res = nouns_extract([text])
    for n in res:
        print n.encode('utf-8'), res[n]
