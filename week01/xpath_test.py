import requests
import lxml.etree
from time import sleep



def get_url_name(myurl):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    header = {'user-agent':user_agent}
    response=requests.get(myurl,headers=header)
    print(response.status_code)
    #print(response.text)

    selector = lxml.etree.HTML(response.text)
    film_link = selector.xpath('//div[@class="hd"]/a/@href')
    film_name = selector.xpath('//div[@class="hd"]/a/span[1]/text()')
    film_score = []
    for i in film_link:
        rsp2 = requests.get(i,headers=header)
        se2 = lxml.etree.HTML(rsp2.text)
        film_score = film_score + se2.xpath('//div[@class="rating_self clearfix"]/strong/text()')
    
    mylist = zip(film_name,film_score,film_link)
    print(list(mylist))


urls = tuple(f'https://movie.douban.com/top250?start={ page * 25}&filter=' for page in range(1))
print(urls)

# from time import sleep
# sleep(10)

for page in urls:
    get_url_name(page)
    # sleep(3)

       