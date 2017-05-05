# search-who
for SOA big project

### 20170426

+ 已完成工作

    加入了github项目，search分支

+ 本周工作

    信息收集 baidu, bing, weibo
    信息分析, 设计格式

### 20170503

+ 已完成工作 

    从百度新闻搜索中提取主要信息和图片

    - config.yaml 为配置文件
    - baidunews.py 为主程序
    - search.html 为调试时的临时文件
    - search.yaml 为输出文件
    - search*.yaml 是输出文件的例子

    yaml文件的读取和存储

    - pip install yaml
    - yaml 结构，-代表list中的元素，:代表dict中的元素
    - yaml 结构示例 [{'a':'x', 'b':1}, {'a':'y'}， {'b':2}]
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