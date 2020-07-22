import requests
import lxml.etree

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
header = {'user-agent':user_agent}
myurl='https://movie.douban.com/subject/1291546/'
response=requests.get(myurl,headers=header)
#print(response.text)


selector = lxml.etree.HTML(response.text)
#selector = lxml.etree.HTML(requests.get(myurl,headers=header).text)
film_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')
print(f'电影名称：{film_name}')

film_date = selector.xpath('//*[@id="info"]/span[10]/text()')
print(f'电影名称：{film_date}')

film_score = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
print(f'电影名称：{film_score}')

mylist = [film_name,film_date,film_score]

import pandas as pd
movie1 = pd.DataFrame(data=mylist)

movie1.to_csv('./movie1.csv',encoding='utf8',index=False,header=False)

