#学习笔记  
##requests 
https://requests.readthedocs.io/zh_CN/latest/user/quickstart.html
安装
pip install requests

导入
import requests

获取某个网页，返回 一个 response 对象
r = requests.get('url')

需要构造 headers 信息，才能更加真实的模拟浏览器
查找header信息
浏览器->F12->Network->选中一个name下的obj->查看右侧的标头/Headers->往下找request headers

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
header = {'user-agent':user_agent}
myurl='https://movie.douban.com/top250'
response=requests.get(myurl,headers=header)

查看请求headers
print(response.request.headers)

查看返回headers
print(response.headers)


查看返回的状态码
response.status_code

查看response的内容,即网页源代码
response.text
------------------------------  

bs4.BeautifulSoup4
用beautifulsoup对源代码做进一步处理
https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#get-text
安装
pip install bs4

导入 注意 BeautifulSoup4 大小写
from bs4 import BeautifulSoup4 as bs

使用bs解析一个网页源代码，得到一个bs对象
Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象
bs_info = bs(response.text,'html.parser')
soup = BeautifulSoup("<html>data</html>")
soup = BeautifulSoup(open("index.html"))

通过find、find_all过滤tag
查找所有 a tag
bs_info.find_all('a')

查找第一个 a tag
bs_info.find('a')
bs_info.find_all('a',limit=1)

唯一的区别是 find_all() 方法的返回结果是包含一个元素的列表,而 find() 方法直接返回结果.

find_all() 方法没有找到目标是返回空列表, find() 方法找不到目标时,返回 None .

下面三条等价，但是第一条可提取特殊属性，如 data-* 属性data-foo="value"
for tags in bs_info.find_all('div',attrs={'class':'hd'}):
for tags in bs_info.find_all('div','hd'):
for tags in bs_info.find_all('div',class_='hd'):


#显示tag的字符串
tag.text
tag.string
tag.get_text([strip=True])

获取tag的属性，操作方法与字典一样
tag.get('href')
tag['href']

#bs4 的替代方法
lxml.etree 之 xpath 查找 tag

安装
pip install lxml

导入
import lxml.etree

用 lxml.etree 对源代码做进一步处理，注意是对源代码处理，所以是response.text，单独的response只是个状态码，等于response.status_code
selector = lxml.etree.HTML(response.text)
selector = lxml.etree.HTML(requests.get('url).text)

浏览器，F12，选择要的tag，右键，复制xpath
用 xpath 方法查找所需内容，注意末尾加上/text()，返回文本内容
film_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')

分别用上述方法获取电影的名称、上映日期、评分
注意：换了一个url后，xpath的内容可能就变了，因为tag数量不一样
不要用 copy as xpath 的方法，手写更加可靠

放入一个数组 mylist
mylist = [film_name,film_date,film_score]

使用pandas将mylist保存到csv文件
安装pandas
pip install pandas
导入
import pandas as pd

生成数据对象
movie1 = pandas.DataFrame(data=mylist)

pandas数据对象调用 to_csv 方法 生成csv文件
encoding 可是 utf8 或 gbk 看哪个显示正确吧
movie1.to_csv('./movie1.csv',encoding='utf8',index=False,header=False)

（待研究 lxml.etree、pandas)

翻页功能
1.将获取当前页面 电影名称 url 的功能封装成一个函数
2.构造所有页面的url
3.用循环将url依次传入到函数，得到每一页的电影名称和url


scrapy  
https://docs.scrapy.org/en/latest/topics/architecture.html  
pip install scrapy  

创建项目
scrapy startproject spiders

创建爬虫spider
cd spiders
cd spiders
scrapy genspider <spider-name> <domain>
scrapy genspider movies douban.com
会产生一个 spiders/movies.py 文件，即爬虫
里面定义了:
    name = 'movies'
    allowed_domains = ['movies.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    
    def parse(self, response):
        pass

若要定义一个函数 早于 回调方法 运行
    def start_requests(self):
        ...
        yield scrapy.request(url=url,callback=self.parse)
        #可用callback指定新的回调方法而非默认方法
        #上面的方法 名字是固定的 且 只会运行一次

scrapy 自带 selector 处理网页内容，类似 xpath  
它要单独导入
from scrapy.selector import selector  
它直接接收response 对象  
movies = selector(response=response).xpath('//div[@class="hd"])  
它返回一个包含匹配tag的list
如何调试
print 或 在浏览器里 ctrl+F  
如何从返回结果中提取文本  
r.extract()  如果匹配了多个tag，全部释放
r.extract_first()  如果匹配了多个tag，只释放第一个 
r.extract_first().strip() 处理掉前后的空格 


运行spider
scrapy crawl movies

当运行命令上述时，Scrapy会在其内部查找对应的 Spider定义 并通过 crawler engine 运行它。

movies爬虫 首先对start_urls属性中定义的 URL 发出请求，并将 响应对象 作为参数传递给默认的 回调方法 parse，然后。
在 回调方法 中，我们使用CSS选择器遍历quote元素，生成包含提取的引用文本和作者的Python dict，查找指向下一页的链接，并使用与回调相同的parse方法安排另一个请求。

在这里，您会注意到Scrapy的主要优势之一：请求是异步调度和处理的。这意味着Scrapy无需等待请求完成和处理，它可以同时发送另一个请求或执行其他操作。这也意味着即使某些请求失败或发生错误，其他请求也可以继续执行 处理它。


settings
放开 USER_AGENT、DOWNLOAD_DELAY=1

return item 会到 pipeline
pipeline 里的方法一定要返回 item 否则报错










