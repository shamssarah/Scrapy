import json
import scrapy
from urllib.parse import urljoin
import re

class AmazonSearchProductSpider(scrapy.Spider):
    name = "yellow_page_restaurants"
    crawl_page = "https://www.yellowpages.ca/search/si/1/Restaurants/Toronto+ON"
    
    def start_requests(self):

        yield scrapy.Request(url=self.crawl_page, callback=self.parse_response, meta={'page': 1})

    def parse_response(self, response):
        page = response.meta['page']
    
        print('***************')
        print('****** Scraping page ' + str(page) )
        print('***************')

        
        list_entity = response.xpath ('//*[@class="listing listing--bottomcta placement placementText  listing--order"]')
        for entity in list_entity:
            item = {}
            card_info = entity.xpath('.//*[@class="listing_right_top_section"]"]')


            card_left_info = card_info.xpath('.//div[@class="listing__right hasIcon "]')

            card_left_info_title = card_left_info.xpath('.//div[@class="listing__title--wrap"]')
            item["name"] = card_left_info_title.xpath('.//a//text()').get().strip()
            item["link"] = "https://www.yellowpages.ca" + card_left_info_title.xpath('.//a//@href').get().strip()
            
            card_left_info_address = card_left_info.xpath('.//div[@class="listing__address address mainLocal"]')
            item["address"] = "".join(card_left_info_address.xpath('.//span[@class="listing__address--full"]//text()').getall()).strip()
            item["location"] = "https://www.yellowpages.ca"+card_left_info_address.xpath('.//a//@href').get()


            card_ex_right_info = card_info.xpath('.//div[@class="listing__extreme-right"]')

            card_ex_right_info_rating = card_ex_right_info.xpath ('.//div[@class="listing__rating ratingWarp"]')
            item["rating"] = card_ex_right_info_rating.xpath('.//span//@aria-label').get()
            item["rating_votes"] = card_ex_right_info_rating.xpath('.//a[@class="listing__ratings__count listing__link"]//text()').get().strip()

            card_ex_right_info_rating_2 = card_ex_right_info.xpath ('.//div[@]')
            item["trip_ad_rating"] = card_ex_right_info_rating_2.xpath('.//img//@src').get()
            item["trip_ad_rating_votes"] = card_ex_right_info_rating_2.xpath('.//span[@class="listing__link listing-quote"]//text()').get()

            card_ex_right_info_timing = card_ex_right_info.xpath ('.//div[@class="merchant__status tooltip__toggle see-hours"]')
            item["timing"] = card_ex_right_info_timing.xpath('.//a//text()').get()


            card_bottom_info = entity.xpath('.//div[@class="listing__bottom"]')

            card_bottom_info_dump = card_bottom_info.xpath('.//div[@class="listing__mlr__root"]//li')
            for info_dump in card_bottom_info_dump:
                if info_dump.xpath(".//span//text()").get():
                    label = info_dump.xpath(".//span//text()").get().lower()
                    if "phone number" == label:
                        item["phone"] = info.dump.xpath(".//a//@data-phone").get()
                    elif "website" == label:
                        item["website"] = "https://www.yellowpages.ca" + info.dump.xpath(".//a//@href").get()


        if response.xpath('//div[@class="view_more_section_noScroll"]//a//@href'):

            next_page_url = "https://www.yellowpages.ca" +  response.xpath('//div[@class="view_more_section_noScroll"]//a//@href').get()
            print (next_page_url)
            # yield scrapy.Request(url=next_page_url, callback=self.parse_response, meta={'page': page+1})
