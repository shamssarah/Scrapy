
import json
import scrapy

# import pandas as pd
from csv import DictWriter

class LinkedCompanySpider(scrapy.Spider):
    name = "linkedin_job_profile"

    #add your own list of company urls here
    crawl_pages = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=IT&location=United States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start="
        # 'https://www.linkedin.com/company/usebraintrust?trk=public_jobs_jserp-result_job-search-card-subtitle',
        # 'https://www.linkedin.com/company/centraprise?trk=public_jobs_jserp-result_job-search-card-subtitle'
        # "https://www.linkedin.com/jobs/search?keywords=IT&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
        




    def start_requests(self):
        
        # company_index_tracker = 0

        # first_url = self.company_pages[company_index_tracker]
        page_no_index = 975

        # for url in crawl_pages:
        url = self.crawl_pages + str(page_no_index)
        yield scrapy.Request(url=url, callback=self.parse_response,meta = {"page_no_index":page_no_index})


    def parse_response(self, response):
        page_no_index = response.meta['page_no_index']
        print('***************')
        print('****** Scraping page ' + str(page_no_index/25+1) )
        print('***************')

        

        entity = response.xpath ('//li')
        num_of_jobs = len(entity)
        list_of_jobs = []
        for job in entity:
            # try:
            job_item = {}
            
            try:
                card_info = job.xpath('.//div[@class="base-search-card__info"]')

                job_item["job_title"] = card_info.xpath('.//*[@class="base-search-card__title"]//text()').get().strip() or "NaN"

                job_item["job_offer_link"] = job.xpath('.//a//@href').get() or "NaN"

                card_subtitle = card_info.xpath('.//*[@class="base-search-card__subtitle"]')
                job_item["job_company"] = card_subtitle.xpath(".//a//text()").get().strip() or "NaN"
                job_item["job_company_link"] = card_subtitle.xpath(".//a//@href").get().strip() or "NaN"

                card_metadata = card_info.xpath('.//*[@class="base-search-card__metadata"]')
                if card_metadata.xpath('.//*[@class="job-search-card__location"]//text()').get():
                    job_item["job_location"] = card_metadata.xpath('.//*[@class="job-search-card__location"]//text()').get().strip()
                else:
                job_item["job_location"] = "NaN"

                if  card_metadata.xpath('.//*[@class="result-benefits__text"]//text()').get().strip()  :
                    job_item["job_application_status"] =  card_metadata.xpath('.//*[@class="result-benefits__text"]//text()').get().strip()  
                else:
                    job_item["job_application_status"] = "NaN"
                    
                if card_metadata.xpath('.//*[@class="job-search-card__listdate"]//text()').get() :
                    job_item["job_list_date"] = card_metadata.xpath('.//*[@class="job-search-card__listdate"]//@datetime').get()
                else:
                    job_item["job_list_date"] = "NaN"
            except:
                print ("Data missing",job_item)
            # yield job_item
            list_of_jobs.append(job_item)
            # except:
            #     print ("Skipping job - not complete data mentioned ")
        
     
 
        # list of column names
        field_names = ['job_title', 'job_offer_link', 'job_company',
                    'job_company_link', 'job_location',"job_application_status","job_list_date"]
           
        # Open CSV file in append mode
        # Create a file object for this file
        with open('linkedln_jobs.csv', 'a',newline='',encoding="utf-8") as f_object:

            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        
            # Pass the dictionary as an argument to the Writerow()
            dictwriter_object.writerows(list_of_jobs)
        
            # Close the file object
            f_object.close()

        if num_of_jobs > 0:
            page_no_index += 25
            url = self.crawl_pages + str(page_no_index)
            yield scrapy.Request(url=url, callback=self.parse_response,meta = {"page_no_index":page_no_index})





