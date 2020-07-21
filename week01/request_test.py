import requests
from bs4 import BeautifulSoup as bs
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
header = {'user-agent':user_agent}
myurl='https://movie.douban.com/top250'
response=requests.get(myurl,headers=header)
#print(response.text)
#print(f'返回码是: {response.status_code}')

bs_info = bs(response.text,'html.parser')
for tags in bs_info.find_all('div',attrs={'class':'hd'}):
#for tags in bs_info.find_all('div',class_='hd'):
    for atag in tags.find_all('a'):
        print(atag.get('href'))
        print(atag.find('span').text)