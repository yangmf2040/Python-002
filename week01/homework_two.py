import scrapy
from spiders.items import SpidersItem


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):

        flink = list()
        fname = list()
        
        for r in response.xpath('//div[@class="channel-detail movie-item-title"]'):
        
            # yield {
            #     'link': r.xpath('./a/@href').getall(),
            #     'name': r.xpath('./a/text()').getll()
            # }

            flink = flink + r.xpath('./a/@href').getall()
            fname = fname + r.xpath('./a/text()').getall()
            
        flink = list(map(lambda x: 'https://maoyan.com'+x,flink))[:10]
        # flist = list(zip(fname,flink))
        fname = fname[:10]
        # print(fname)
        # print(flink)

        for i in range(0,10):
            item = SpidersItem()
            item['name'] = fname[i]
        # items = []
        # items = items.append(item) 
        # return items
        # return item

            # for link in flink:
            link=flink[i]
            yield scrapy.Request(url=link,callback=self.parse2,meta={'item':item},dont_filter=True)

    def parse2(self, response):
        item = response.meta['item']
        tmplist = []
        for r in response.xpath('//li/a[@class="text-link"]/text()').getall():
            # print(r)
            tmplist.append(r)
        item['ftype'] = tmplist

        tmplist=[]

        for r in response.xpath('//li[contains(text(),"-")]/text()').getall():
            # print(r)
            tmplist.append(r)
        item['date'] = tmplist

        return item

        


