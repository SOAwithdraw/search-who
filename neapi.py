# -*- coding:utf8 -*-
from urllib import parse, request


def ner(text):

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
    content = result.read().decode('utf-8').strip().split('\n')

    print(content)

    res = {}

    for item in content:
        name, char = item.split()
        if name not in res:
            res[name] = [char, 1]
        else:
            res[name][1] += 1

    return res


if __name__ == '__main__':
    text = "四川新闻网泸州4月26日讯（赵学龙 )近日，叙永县县委副书记、县长唐杰带领财政局、交通局、水务局、住建局等单位到黄坭乡督导检查安全生产工作，黄坭乡主要领导陪同检查。督查组一行到燕子岩实地察看，详细了解燕子岩事故隐患整改落实情况。唐杰要求：在当前脱贫攻坚的关键时期，一定要进一步提高安全生产认识，强化值班值守和痕迹管理，确保工作措施落实到人，责任落实到位。要加大对安全隐患的排查力度，及时消除隐患。坚持一手抓管理、检查，一手抓宣传教育，做到严格执法。加强对重点行业、重点企业的监督排查，并形成长效机制，对督查时发现的问题要尽快整改。要加强道路交通安全教育宣传，结合实际案例，通过各种安全宣传活动形式，增强大家的安全意识，养成良好的驾驶习惯。"
    res = ner(text)
    print(res)
