import scrapy
# from scrapy.http.request.form import FormRequest

import pandas as pd

class WebsiteDetails(scrapy.Spider):
    
    name = "website_solution_crawler"

    
    custom_settings = {
        'FEEDS': { 
            'data/%(name)s/%(name)s_%(time)s.csv': 
            {
            'format': 'json',
            }
        }}

    crawl_pages = "https://www.cetera.com/solutions"


    def start_requests(self): 
        yield scrapy.Request(url=self.crawl_pages, callback=self.extract_website)


    def extract_website(self, response):


        all_content = response.xpath('.//div[@class="tab-content"]//*[@class="row row-wrapper"]//*[@class="highlight_content"]')
        for entity in all_content:
            if ( entity.xpath('.//h3[@class="title"]//text()')):
                solution_title = entity.xpath('.//h3[@class="title"]//text()').get().strip()
                solution_desc = entity.xpath ('.//p//text()').get().strip()
                learn_more = entity.xpath('.//a//@href').get()
                yield scrapy.Request (url= "https://www.cetera.com"+learn_more,callback=self.page_response,meta = {"Title" : solution_title,
                        "Description" : solution_desc})
        # return
    def page_response (self, response):

        content =  response.xpath('.//div[@class="panel-group skin-white"]//*[@class="panel panel-default"]')
        output = []
        for panel in content:
            heading = panel.xpath('.//*[@class="panel-heading"]//a//text()').get().strip()
            desc = panel.xpath('.//*[@class="panel-body"]//p//text()').get().strip()
            output.append(heading + " :: " + desc)
        print (output)
        return {"Title" : response.meta["Title"],
                "Description" : response.meta["Description"],
                "Detail" : "\n\n".join(output)}
        


        
      
