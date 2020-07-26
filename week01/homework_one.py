import requests
from bs4 import BeautifulSoup as bs
import re
from time import sleep

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
cookie1 = '__mta=222204839.1595595762485.1595694757096.1595694972213.8; uuid_n_v=v1; uuid=F4951A30CDAD11EA9F0EBD9BEC3DAA2BE8D8DC71DF3342A08475DAE80DBBD610; _csrf=148b6825e27ba340ec46aae9911f9f72efcbb4f7452b567de47ed94fa170c8c2; mojo-uuid=e2ccb801814d4db79b53c48533b17b6c; _lxsdk=F4951A30CDAD11EA9F0EBD9BEC3DAA2BE8D8DC71DF3342A08475DAE80DBBD610; _lxsdk_cuid=17380eb2ac215-08ab6ddf7aeb4e-5d37194f-144000-17380eb2ac3c8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595691586,1595693019,1595693409,1595694299; mojo-session-id={"id":"fee83ebda9057bbade99d38b8350a3c4","time":1595700172225}; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595700173; __mta=222204839.1595595762485.1595694972213.1595700172890.9; _lxsdk_s=1738724576c-f60-be5-926%7C%7C3'
header = {'user-agent':user_agent,'cookie':cookie1}
myurl='https://maoyan.com/films?showType=3'
response=requests.get(myurl,headers=header)
print(response.status_code)
# print(response.text)

fname = []
flink = []
ftype = []
ftime = []

bs_info = bs(response.text,'html.parser')
# for tags in bs_info.find_all('div',attrs={'class':'channel-detail movie-item-title'},limit=1):
for tags in bs_info.find_all('div',attrs={'class':'channel-detail movie-item-title'},limit=10):
    # print(tags.get_text())
    # print(tags)
    # print(tags.find('a').get('href'))
    fname.append(tags.get_text(strip=True))
    flink.append(tags.find('a').get('href'))
    

for link in flink:
    sleep(3)
    myurl2 = 'https://maoyan.com'+link
    response2=requests.get(myurl2,headers=header)
    bs_info2 = bs(response2.text,'html.parser')
    tmplist = []
    for atag in bs_info2.find_all('a',class_="text-link"):
        for i in atag:
            tmplist.append(i)
    ftype.append(tmplist)
    for atag in bs_info2.find_all('li',class_="ellipsis",string=re.compile(r"\d{4}")):
        ftime.append(atag.text)
        # print(atag.text)
# print(fname)
# print(ftype)
# print(ftime)

flist = list(zip(fname,ftype,ftime))

with open("./movies.txt","a+",encoding="utf8") as f:
    for i in flist:
        f.write(str(i).strip('()'))
        f.write('\n')