import scrapy
# from scrapy.http.request.form import FormRequest

import pandas as pd

class WebsiteDetails(scrapy.Spider):
    name = "website_detail_crawler"

    crawl_pages = [
        "https://www.expert-seo-training-institute.in/blog/business-listing-sites-list/"
        ]


    def start_requests(self): 
        # print (crawl_pages)
        for url in self.crawl_pages: 
            print (url)
            yield scrapy.Request(url=url, callback=self.extract_website)


    def extract_website(self, response):
        list_website = []
        table = response.xpath('//td[@class="column-2"]/a') + response.xpath('//td[@class="column-1"]/a')

        for row in table:
            # print ("---------------\n--------\n---------\n")
            text = row.xpath('text()').get()
            url = row.xpath('@href').get()
            
            privacy_link = scrapy.Request(url = url,callback = self.extract_website_detail, meta = {"name": text})
            list_website.append([text,url,privacy_link])
            # break
        # print (list_website)
        df = pd.DataFrame(list_website,columns = ["name","website","privacy_link"])
        print (df)
        df.to_csv("list_website.csv",index = None)
        return

    def extract_website_detail (self,response):
        website_name = response.meta['name']
        print ("Extraction of ", website_name)
        privacy_link = response.xpath ('//a[contains(@href,"privacy") or contains(@href,"Privacy")]/@href')
        list_ = []
        for web in privacy_link:
            list_.append(privacy_link.get())
        
        return pd.unique(pd.Series(list_))
      
