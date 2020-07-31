from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from bds.items import BdsItem
import scrapy
from scrapy.exceptions import DropItem
import re

class BDSSpider(CrawlSpider):
    name = "bds"
    allowed_domains = ['batdongsan.com.vn']
    start_urls = []
    for i in range(1000,2779):
        start_urls.append('https://batdongsan.com.vn/nha-dat-ban-ha-noi/p{}'.format(i))
    base_url = 'https://batdongsan.com.vn/nha-dat-ban-ha-noi'

    # def parse(self,response):
    #     number_pages = response.xpath('//*[@id="form1"]/div[3]/div[4]/div[2]/div/div[1]/div[1]/div/span[2]/strong/text()').extract()[0]
    #     number_pages = int(re.sub(',','',number_pages))//20 +1
    #     for i in range(2500,number_pages):
    #         url = self.base_url + '/p{}'.format(i)
    #         yield scrapy.Request(url, callback=self.parse_link)

    def parse(self, response):
        # next_link = Selector(response).xpath('//*[@id="form1"]/div[3]/div[4]/div[2]/div/div[3]/div/a[6]/@href').extract()
        # for link in next_link:
        #     url = response.urljoin(link)
        #     yield scrapy.Request(url, callback=self.parse)

        links = Selector(response).xpath('//*[@class="p-title"]/h3/a/@href')
        for link in links:
            item = link.extract()
            full_url  = response.urljoin(item)
            yield scrapy.Request(full_url, callback=self.parse_item)


    def parse_item(self,response):
        item = BdsItem()
        try:
            item['title'] = response.xpath('//*[@id="product-detail"]/div[1]/h1/text()').extract()[0]
            item['price'] = response.xpath('//*[@id="product-detail"]/div[2]/span[2]/span[1]/strong/text()').extract()[0]
            item['square'] = response.xpath('//*[@id="product-detail"]/div[2]/span[2]/span[2]/strong/text()').extract()[0]
            item['address'] = response.xpath('//*[@id="hdAddress"]/@value').extract()[0]
            item['category'] = response.xpath('//*[@id="product-other-detail"]/div[1]/div[2]/text()').extract()[0]
            item['longitude'] = response.xpath('//*[@id="hdLong"]/@value').extract()[0]
            item['latitude'] = response.xpath('//*[@id="hdLat"]/@value').extract()[0]
            item['dateCreate'] = response.xpath('//*[@id="product-detail"]/div[9]/div[3]/text()').extract()[1]
        except:
            raise DropItem('Can\'t get element')
        yield item
