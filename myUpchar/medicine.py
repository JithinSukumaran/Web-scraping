import scrapy
from scrapy import Request
import pandas as pd
import numpy as np

class MedicineSpider(scrapy.Spider):
    name = 'medicine'
    allowed_domains = ['myupchar.com/en']
    start_urls = ['https://www.myupchar.com/en/search?term=Ketamine&filter=medicine']
    

    def parse(self, response):
        df = pd.read_excel('salts.xlsx')
        salts = df['Salt Name']
        for salt in salts[2:]:
        # for salt in lst:
            url = f'https://www.myupchar.com/en/search?term={salt}&filter=medicine'
            yield Request(url, callback=self.parse_search, dont_filter = True,meta={'salt':salt})

    def parse_search(self, response):
        '''
        this function is for gethering the links of result in the search page and iterate upon them and
        to go to the next page of the search results if it is there.
        '''
        salt1 = response.meta.get('salt')

        search = response.xpath('//*[@class ="surgery-section-bx"]/@href').extract()
        # search is a set of all the links in the search page
        
        for link in search:
            absolute_url = response.urljoin(link)
            yield Request(absolute_url, callback=self.listing, dont_filter = True,meta={'URL':absolute_url,'salt1':salt1})
      
        if response.xpath('//a[@aria-label ="Next"]/@href').extract():   # cheking for next page
            next_page_url = response.xpath('//a[@aria-label ="Next"]/@href').extract()[0]
            absolute_next_page_url = response.urljoin(next_page_url)
            yield Request(absolute_next_page_url,callback=self.parse_search, dont_filter = True)

    def listing(self,response):
        '''
        This method is used to finally extract information from the individual medicine and yield them
        '''
        url = response.meta.get('URL')
        salt2 = response.meta.get('salt1')

        name = response.xpath('//*[@class ="head"]/h1/text()').extract()[0]
        manufracturer = response.xpath('//*[@class="medicine_info"]/li/b/a/text()').extract()[0]
        salt= response.xpath('//*[@class="medicine_info"]/li/b/text()').extract()[-1]
        price = response.xpath('//*[@class="txt_big"]/text()').extract()[0]
        packSize = response.xpath('//span[@class="middle_txt"]/text()').extract_first()


        # prescription info (check on page where precription is not required)
        prescription = response.xpath('//*[@class="pres_txt"]/text()').extract()[0]

        # pregnant, breastfeeding, kidneys , liver ,heart (this will work side_effects = only if all are present and in the same order)
        warnings = response.xpath('//*[@class="inline_item"]/div/span/text()').extract()[:5]
        pregnant_warning = []
        pregnant_text = []
        breastfeeding_warning = []
        breastfeeding_text = []
        kidney_warning = []
        kidney_text = []
        liver_warning = []
        liver_text = []
        heart_warning = []
        heart_text = []
        if len(warnings) == 5:
            pregnant_warning = warnings[0]
            breastfeeding_warning = warnings[1]
            kidney_warning = warnings[2]
            liver_warning = warnings[3]
            heart_warning = warnings[4]

        warnings_text = response.xpath('//*[@class="inline_item"]/div/p/text()').extract()[:5]
        if len(warnings_text) == 5:
            pregnant_text = warnings_text[0]
            breastfeeding_text = warnings_text[1]
            kidney_text = warnings_text[2]
            liver_text = warnings_text[3]
            heart_text = warnings_text[4]

        # Interaction with food and alcohol
        food_alcohol = response.xpath('//*[@class="inline_item"]/div/span/text()').extract()[-2:]
        food_warning = []
        food_text = []
        alcohol_warning = []
        alcohol_text = []

        if len(food_alcohol) ==2:
            food_warning = food_alcohol[0]
            alcohol_warning = food_alcohol[1]

        food_alcohol_text = response.xpath('//*[@class="inline_item"]/div/p/text()').extract()[-2:]
        if len(food_alcohol_text) ==2:
            food_text = food_alcohol_text[0]
            alcohol_text = food_alcohol_text[1]

        yield {
            'Salt Name':salt2,
            'Name':name,
            'Manufracturer':manufracturer,
            'Contains/Salt':salt,
            'Price':price,
            'Pack size label': packSize,
            'Prescription':prescription,
            'Link': url,
            'Pregnant text':pregnant_text,
            'Pregnant warning': pregnant_warning,
            'Breastfeeding text': breastfeeding_text,
            'Breastfeeding warning': breastfeeding_warning,
            'Kidney text':kidney_text,
            'Kidney warning': kidney_warning,
            'Liver text': liver_text,
            'Liver warning': liver_warning,
            'Heart text': heart_text,
            'Heart warning': heart_warning,
            'Food text': food_text,
            'Food warning': food_warning,
            'Alcohol text': alcohol_text,
            'Alcohol warning': alcohol_warning
            }
