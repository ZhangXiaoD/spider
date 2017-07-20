# spider

## us_tv
1. 爬取天天美剧的剧集信息，抓取结果保存在us_tv中自动生成的美剧资源.csv文件内。
2. 直接运行us_tv目录中的spider文件即可
3. 依赖库:requests,bs4

## jdbook_python
1. 爬取京东移动端，京东配送的信息，默认爬去的信息关键字是python，
   可以在config文件内修改KEYWORD关键词搜索其他内容，只进行了简单测试，其他关键词部分信息解析可能会出错。
2. 去重用的是redis，抓取结果保存在mangodb中，所以需要自行安装redis以及mongodb并启动。
3. 运行jdbook_python目录中的spider文件。
4. 依赖库：requests,bs4,redis,pymongo

## douban_music以及163_music
1. 框架选用的是pyspider，支持python3
2. 自行安装pyspider，打开pyspider的web页面，create新项目，Project Name按个人喜好随便选取，Start URL(s)为文件中以下方法中的url
```python
    def on_start(self):
        self.crawl('http://music.163.com/discover/playlist', callback=self.index_page)
```
  Project Name以及Start URL(s)填好之后点击create创建项目，然后把代码粘贴到web中，点击save，返回pyspider控制台
  修改status为running，点击actions中的run就启动了。
3. 数据保存在mongodb中，所以需要自行安装mongodb，以及python的mongo依赖库pymongo
4. 如果对pyspider的使用有疑问请留言或者自行搜索pyspider了解具体的使用方法
