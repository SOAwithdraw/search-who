# -*- coding:utf8 -*-
from urllib import parse, request
import time


def ner(*texts):
    '''
    Get the Named-entitys from ltp-cloud

    Args:
        texts: all the texts needed to be analyzed.

    Returns:
        res_all: a list containing dicts of named-entitys for each text.
    '''

    joint = "吉日杜万是一个分界线。"
    text = joint.join(texts)
    print(text)

    url_get_base = "http://api.ltp-cloud.com/analysis/"
    args = {
        'api_key': 'N19193n1802Bdn9ToIkxBWcITwUDkjbQPKrarJAQ',
        'text': text,
        'pattern': 'ner',
        'format': 'plain',
        'only_ner': 'true'
    }
    data = parse.urlencode(args).encode('utf-8')
    result = request.urlopen(url_get_base, data)  # POST method
    contents = result.read().decode('utf-8').split('吉日杜万 Nh\n')

    res_all = []

    for content in contents:
        content = content.strip().split('\n')

        res = {}

        for item in content:
            name, char = item.split()
            if name not in res:
                res[name] = [char, 1]
            else:
                res[name][1] += 1

        res_all.append(res)

    return res_all


if __name__ == '__main__':

    start = time.clock()
    text1 = "四川新闻网泸州4月26日讯（赵学龙 )近日，叙永县县委副书记、县长唐杰带领财政局、交通局、水务局、住建局等单位到黄坭乡督导检查安全生产工作，黄坭乡主要领导陪同检查。督查组一行到燕子岩实地察看，详细了解燕子岩事故隐患整改落实情况。唐杰要求：在当前脱贫攻坚的关键时期，一定要进一步提高安全生产认识，强化值班值守和痕迹管理，确保工作措施落实到人，责任落实到位。要加大对安全隐患的排查力度，及时消除隐患。坚持一手抓管理、检查，一手抓宣传教育，做到严格执法。加强对重点行业、重点企业的监督排查，并形成长效机制，对督查时发现的问题要尽快整改。要加强道路交通安全教育宣传，结合实际案例，通过各种安全宣传活动形式，增强大家的安全意识，养成良好的驾驶习惯。"
    text2 = "2017年3月3日，哈尔滨工业大学(深圳)经管学院教授、博士生导师、原深圳市副市长唐杰应邀发表题为《创新增长的制度与理念》的演讲。他旁征博引，畅谈古今，从康乾盛世到英国崛起，从东西方的碰撞到深圳转型，在数千年的历史规律中发现能为当今社会发展所借鉴的经验，在科技推动社会进步的现在寻找中国经济发展的新方向。讲座后，他与在座嘉宾一同讨论了科技与社会发展等延伸话题，并被聘请为国家基因库顾问。"
    text3 = "论坛上，原深圳市副市长、哈尔滨工业大学（深圳）临时党委书记、经管学院教授唐杰表示，中国现在的问题是在城市化过程中的城市体之间的撕裂，这样的撕裂过程在广东省也存在。"
    res = ner(text1, text2, text3)
    for item in res:
        print(item)
    end = time.clock()
    print(end - start)
