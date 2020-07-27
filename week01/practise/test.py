import requests
import lxml.etree

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
header = {'user-agent':user_agent}
myurl='https://movie.douban.com/subject/1291546/'
response=requests.get(myurl,headers=header)
print(response.headers)
print(response.request.headers)