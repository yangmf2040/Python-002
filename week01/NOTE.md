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

查看返回的状态码
response.status_code

查看response的内容,即网页源代码
response.text

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

唯一的区别是 find_all() 方法的返回结果是值包含一个元素的列表,而 find() 方法直接返回结果.

find_all() 方法没有找到目标是返回空列表, find() 方法找不到目标时,返回 None .

下面三条等价，但是第一条可提取特殊属性，如 data-* 属性data-foo="value"
for tags in bs_info.find_all('div',attrs={'class':'hd'}):
for tags in bs_info.find_all('div','hd'):
for tags in bs_info.find_all('div',class_='hd'):


显示tag的字符串
tag.text
tag.string

获取tag的属性，操作方法与字典一样
tag.get('href')
tag['href']

bs4 替代方法
lxml.etree 之 xpath 查找 tag

安装
pip install lxml

导入
import lxml.etree

用 lxml.etree 对源代码做进一步处理，注意是对源代码处理，所以是response.text，单独的response只是个状态码，等于response.status_code
selector = lxml.etree.HTML(response.text)
selector = lxml.etree.HTML(requests.get('url).text)

浏览器，F12，选择要的tag，右键，复制xpath
用 xpath 方法查找所需内容，注意末尾加上/text()，返回内容
film_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')

分别用上述方法获取电影的名称、上映日期、评分
注意：换了一个url后，xpath的内容可能就变了，因为tag数量不一样

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











