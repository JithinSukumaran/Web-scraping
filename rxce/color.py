import scrapy
import json

class ColorSpider(scrapy.Spider):
    name = 'color'
    # allowed_domains = ['rxce.in']
    # start_urls = ['https://rxce.in/win/guesses?t=1633788862000&category=E&p=1&p_size=25']
    # page = 1

    def start_requests(self):
        url = 'https://rxce.in/win/guesses?t=1633788862000&category=E&p=1&p_size=25'
    
        headers ={
            'accept':'application/json, text/plain, */*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'en-GB,en-US;q=0.9,en;q=0.8',
            'authorization':'Token f57b70884b423e46fc31e2154f81e4d1c513aeb4',
            'cookie':'csrftoken=syCRZ7iVD4BV9BoxaCwRMzNjkIFDdMwxf2w4C85aCjJvXPYzKcWDwtJu8n1QVde8',
            'referer':'https://rxce.in/',
            'sec-fetch-dest':'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site':'same-origin',
            'sec-gpc':'1',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }

        for x in range(8):
            url = f'https://rxce.in/win/guesses?t=1633788862000&category=E&p={x+1}&p_size=25'
            yield scrapy.http.Request(url, headers=headers)

    def parse(self, response):
        print('='*100)
        print(response.body)
        resp = json.loads(response.body)
        print('='*100)
        hotels = resp.get('queryset')
        for hotel in hotels:
            yield{
                'period':hotel.get('period'),
                'price':hotel.get('price'),
                "last_num": hotel.get("last_num"),
                "is_green": hotel.get("is_green"),
                "is_red": hotel.get("is_red"),
                "is_violet": hotel.get("is_violet"),
                "create_time": hotel.get("create_time"),
                "create_timestamp": hotel.get("create_timestamp")
            }
