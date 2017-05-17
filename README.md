# search-who
for SOA big project

### 接口总结

+ baidu.py
        
    get(word, index0 = 0, newscnt = 10)
    - 传入参数:
    >
        word 表示查询关键词，中文使用utf-8编码
        index0 表示新闻的起始编号
        newscnt 表示搜索条数
    
    - 返回结果:
    >
        [{id:id, img:[images], text:[texts], title:title， url:url}]
    
    - 其他说明
    >
        由于百度反爬虫机制，大约每一条新闻需要1秒钟
+ weibo.py

    VisitPersonPage(word, num = 20)
    - 传入参数：
    >
        word 表示查询关键词，中文使用utf-8编码
        num 表示搜索数
    
    - 返回结果：
    >
        [{name:昵称，id:编号，img:头像图片url，info:个人签名}]
    - 其他说明：
    >
        返回用户数量约等于num，如果搜索结果总数＜num则返回所有
        平均每10个用户需要1秒钟，预处理需要5秒钟
    
### 20170517
+ 已完成工作

    完成了weibo.py的接口

+ weibo.py

    VisitPersonPage(word, num), 传入关键词，所需用户数，返回用户数量约等于num，如果搜索结果总数＜num则返回所有
    返回格式[{name:昵称，id:编号，img:头像图片url，info:个人签名}]
    更新了样例文件

### 20170516

+ 已完成工作
    对于关键词，获取30个左右的微博
    
+ weibo.py
    
    可以提取微博的昵称(name), 简介(info), 头像(img), 放入weibo.yaml中<br>

    程序约需要10s时间执行<br>

    使用 selenium 和 firefox实现<br>

+ weibo1.yaml 
    
    陈驰的搜索结果

+ weibo2.yaml 
    
    郭文景的搜索结果

+ weibo3.yaml 
    
    唐杰的搜索结果，同时对应增加了唐杰的 search3.yaml

+ 已知问题
    
    目前代码比较简单，参数通过代码修改

### 20170510

+ 已完成工作
    
    对于每条百度新闻，添加了id,title和url
    更新了search1.yaml，search2.yaml
    
+ baidunews.py
    
    get(word, index0 = 0, newscnt = 10)
    word 表示查询单词，中文使用utf-8编码
    index0 表示新闻的起始编号
    newscnt 表示搜索条数
    返回值为 [{id:id, img:[images], text:[texts], title:title， url:url}]

+ 已知问题
    繁体标题乱码，目前假设百度新闻均为gbk格式


### 20170505

+ 已完成工作
    修改了readme的bug
    修改了img的值，填充了http:


### 20170503

+ 已完成工作 

    从百度新闻搜索中提取主要信息和图片

    - config.yaml 为配置文件
    - baidunews.py 为主程序
    - search.html 为调试时的临时文件
    - search.yaml 为输出文件
    - search*.yaml 是输出文件的例子

    yaml文件的读取和存储

    - `pip install yaml` 或 `pip install pyymal`
    - yaml 结构，-代表list中的元素，:代表dict中的元素
    - yaml 结构示例 [{'a':'x', 'b':1}, {'a':'y', 'b':2}]
    ``` yaml
    -   a: 'x'
        b：1
    -   a: 'y'
        b: 2
    ```

    - 读取示例代码，data为读取后的结果，结构和yaml文件对应


    ```python
        import yaml
        fr = open('search.yaml', 'r')
        data = yaml.load(fr)
    ```

    - 存储示例代码，data为python的结构，打印到yaml文件对应

    ```python
        import yaml
        output = codecs.open("search.yaml", "w", "utf-8")
        yaml.dump(searchresult, default_flow_style=False,stream=output,indent=4,encoding='utf-8',allow_unicode=True, width=1000)

    ```


### 20170426

+ 已完成工作

    加入了github项目，search分支

+ 本周工作

    信息收集 baidu, bing, weibo
    信息分析, 设计格式

    