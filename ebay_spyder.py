import scrapy
import requests 
# from request_html import HTMLSession
from lxml import html, etree

proxy = "https://103.227.254.59:80"

class EbayCW(scrapy.Spider):
    name = "ebay_cw"
    start_urls = ["https://www.ebay.com/sch/i.html?rt=nc&_nkw=Samsung+Galaxy+Note20+Ultra"]

    # sess = HTMLSession() 
    # res = s.get(url)
    # r.html.render (sleep=1)
    

    # def start_request (self):
    #     for url in website:
    #         yield fetch(url=url, callback=self.parse)

    def parse (self,response):
        # sess = HTMLSession() 
        # response = s.get(url)
        # response.html.render (sleep=1)
        # response = requests.get ("https:/httpbin.org/ip", proxies = {"http":proxy, "https":proxy})
        for products in response.xpath("//div[@class='s-item_info clearfix'")[0]:

            yield {
            'title' : response.xpath("//h3[@class='s-item__title']//text()"),
            'ownership' : response.xpath("//div[@class='s-item__subtitle']//text()"),
            'price' : " ".join(response.xpath("//span[@class='s-item__price']//span//text()")),
            'review' : response.xpath("//div[@class='x-star-rating']//span[@class='clipped']//text()").split()[0]
        }   


        next_page = response.xpath("a[@class='pagination__next']")["href"]
        if next_page is not None:
            yield response.follow (next_page,callback=self.parse)
