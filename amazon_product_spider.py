import json
import scrapy
from urllib.parse import urljoin
import re

class AmazonSearchProductSpider(scrapy.Spider):
    name = "amazon_search_product"

    
    custom_settings = {
        'FEEDS': { 
            'data/%(name)s/%(name)s_%(time)s.csv': 
            {
            'format': 'csv',
            }
        }}

    def start_requests(self):
        keyword_list = ['ipad']
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': 1})

    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 

        list_product = response.xpath ('//*[@class="a-section a-spacing-small a-spacing-top-small"]')
        for product in list_product:

            item = {}
            if (product.xpath('.//*[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')):
                product_name = product.xpath('.//*[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
                item["product_name"] = product_name.xpath(".//text()").get().strip()
                item["product_link"] = product_name.xpath(".//@href").get().strip()
                item["rating"] = product.xpath('.//*[@class="a-section a-spacing-none a-spacing-top-micro"]//span[@ class="a-size-base"]//text()').get()
                item["no_of_review"] = product.xpath('.//*[@class="a-section a-spacing-none a-spacing-top-micro"]//span[@class="a-size-base s-underline-text"]//text()').get()
                if product.xpath('.//*[@class="a-price-whole"]'):
                    item["price"] = float(product.xpath('.//*[@class="a-price-whole"]//text()').get().replace(",","")) + float(product.xpath('.//*[@class="a-price-fraction"]//text()').get())/100  
                else:
                    item["price"] = "NaN"
                if product.xpath('.//div[@class="a-row a-size-base a-color-secondary"]//*[@class="a-size-base a-color-price"]//text()'):
                    item["item_stock"] = product.xpath('.//div[@class="a-row a-size-base a-color-secondary"]//*[@class="a-size-base a-color-price"]//text()').get().strip()
                else:
                    item["item_stock"] = "NaN"
                yield item
        if page == 1:
            available_pages = response.xpath(
                '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            ).getall()

            for page_num in available_pages:
                amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': page_num})
        
