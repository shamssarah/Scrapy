import scrapy
# from scrapy.http.request.form import FormRequest

import pandas as pd

class WebsiteDetails(scrapy.Spider):
    name = "website_business_det_crawler"

    custom_settings = {
        'FEEDS': { 
            'data/%(name)s/%(name)s_%(time)s.csv': 
            {
            'format': 'csv',
            }
        }}

    crawl_pages = [
        "https://www.houzz.co.uk/professionals/bathroom-designers/project-type-complete-bathroom-renovation-probr1-bo~t_11853~sv_32787"
        ]


    def start_requests(self): 
        # print (crawl_pages)
        page = 1
        for url in self.crawl_pages: 
            print (url)
            yield scrapy.Request(url=url, callback=self.extract_website,meta={'page': page+1})


    def extract_website(self, response):
        print ("-------------------")
        print ("Scraping ", response.meta["page"])
        print ("-------------------")

        list_of_entity = response.xpath ('.//ul[@class="hz-pro-search-results mb0"]//li')
        for entity in list_of_entity:
            link = entity.xpath(".//a//@href").get()
            if link:
                yield scrapy.Request(url=link, callback = self.extract_link_detail, meta = {"link":link})
        
        if response.xpath('.//*[@class="hz-pagination-link hz-pagination-link--next"]//a//@href') :
            next_page_url = "https://www.houzz.co.uk" +  response.xpath('.//*[@class="hz-pagination-link hz-pagination-link--next"]//a//@href').get()
            print (next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.extract_website, meta={'page': page+1})

    

    def extract_link_detail (self,response):

        print ("-------------------")
        print ("Scraping ", response.meta["link"])
        print ("-------------------")
        
     

        initial = response.xpath('.//div[@class="sc-183mtny-0 fAraQc"]')  
        name = initial.xpath(".//h1//text()").get().strip()
        rating_no = initial.xpath('.//*[@class="hz-star-rate__rating-number"]//text()').get()
        review_no = initial.xpath('.//*[@class="hz-star-rate__review-string"]//text()').get()
        work = "".join(initial.xpath('.//*[@class="sc-mwxddt-0 hvabAf"]//text()').getall()).strip() 

        card_info = response.xpath('.//section[@id="business"]//div') 
        item = {}    
        item ["Type of Work"] = work
        item ["Rating"] = rating_no
        item ["No. of Review"] = review_no 
        for info in card_info:
            if info.xpath(".//p//a//@href"):
                value = info.xpath(".//p//a//@href").get()
            else:
                value = "".join(info.xpath(".//p//text()").getall()).strip()
            if info.xpath(".//h3//text()"):
                item[info.xpath(".//h3//text()").get().strip()] = value
        item ["webpage"] = response.meta["link"]
        return item
        