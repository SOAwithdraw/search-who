# Search-Who
<font color="Red">__DDL is coming !!!__</font>

### 已完成

- 百度新闻的收集、整理、聚类

    - news_search.py
        
        search(name, describe=[], cache_dir="data")

        - name：待搜索人名
        - describe：可能有的一些描述词，如“唐杰 清华大学”中的“清华大学”
        - cache_dir：
            存放抓取的页面和聚类结果的文件夹


### 待完成

- search函数返回url、类关键词(@cc)

- baidunews增加title部分(@jzc)

- 聚类考虑title的加权和名字附近字的加权(@general，__暂时延后__)

- 图片信息的引入

- 关联微博和知乎

- 前端页面
