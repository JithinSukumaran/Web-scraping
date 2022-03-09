import scrapy
from scrapy import Request

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['flipkart.com']
#    start_urls = [url]
    # start_urls = ['https://www.flipkart.com/apple-iphone-12-mini-black-64-gb/product-reviews/itm38b727191eb08?pid=MOBFWBYZXSEGBS6F&lid=LSTMOBFWBYZXSEGBS6FTONJ6W&marketplace=FLIPKART&page=549']
    count = 0

    def parse(self, response):
        reviews = response.xpath('//div[@class="col _2wzgFH K0kLPL"]')

        for review in reviews:
            data ={
            'Stars' : review.xpath('.//div[@class="row"]/div/text()').extract_first(),
            'Comment' :review.xpath('.//p[@class="_2-N8zT"]/text()').extract_first(),
            'Review' : review.xpath('.//div[@class=""]/text()').extract_first(),
            'Name' : review.xpath('.//p[@class="_2sc7ZR _2V5EHH"]/text()').extract_first(),
            'Certified_buyer' : review.xpath('.//p[@class="_2mcZGG"]/span[1]/text()').extract_first(),
            'City' : review.xpath('.//p[@class="_2mcZGG"]/span[2]/text()').extract_first(),
            'Date' : review.xpath('.//p[@class="_2sc7ZR"]/text()').extract_first(),
            'Likes of other users' : review.xpath('.//span[@class="_3c3Px5"]/text()').extract()[0],
            'dislikes of other users' : review.xpath('.//span[@class="_3c3Px5"]/text()').extract()[1]
            }

            yield data

        if response.xpath('//a[@class="_1LKTO3"]/span/text()').extract()[-1] == 'Next':
            # self.count +=1
            next_url = response.xpath('//a[@class="_1LKTO3"]/@href').extract()[-1]
            absolute_next_url = response.urljoin(next_url)
            yield Request(absolute_next_url,callback=self.parse,dont_filter=True)

# class for 2 star
# class="_3LWZlK _32lA32 _1BLPMq"

# class for 1 star
# class="_3LWZlK _1rdVr6 _1BLPMq"
