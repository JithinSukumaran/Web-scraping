import scrapy
import re


class ContactSpider(scrapy.Spider):
    name = 'contact'

    def start_requests(self):
        for x in range(5):
            yield scrapy.Request(f'https://meitystartuphub.in/startups/startup-wall?search=&page={x+1}&domain=&location=&stage=&type=',
            callback=self.parse)


    def parse(self, response):
        companies = response.xpath('//div[@class ="row w-100 col-12 mx-0 align-items-center body-row mb-2"]')

        for company in companies:
            name = company.xpath('.//div[@class="col pl-0"]/text()').extract_first()
            sector =  ''.join(company.xpath('.//div[@class="row justify-content-center align-items-center col-2 mx-0 body-col text-center sectors "]/text()').extract()).strip()
            address = company.xpath('.//div[@class="row col-3 mx-0 align-items-center body-col justify-content-center "]/text()').extract_first().strip()

            try:
                website = company.xpath('.//a/@href').extract()[-1]
            except:
                pass

            if 'http' not in website:
                website = 'https://' + website

            try:
                yield scrapy.Request(website,callback=self.parse_website, meta={'name':name, 'sector':sector,'address':address})
            except:
                pass
            
            # yield{
            #     'Name':company.xpath('.//div[@class="col pl-0"]/text()').extract_first(),
            #     'Employees': company.xpath('.//div[@class="row col-2 mx-0 align-items-center body-col justify-content-center "]/text()').extract_first().strip(),
            #     'Industies': ''.join(company.xpath('.//div[@class="row justify-content-center align-items-center col-2 mx-0 body-col text-center sectors "]/text()').extract()).strip(),
            #     'Address': company.xpath('.//div[@class="row col-3 mx-0 align-items-center body-col justify-content-center "]/text()').extract_first().strip(),
            #     'Website': company.xpath('.//a[@class="text-center"]/text()').extract_first()
            # }

    def parse_website(self,response):
        name = response.meta.get('name')
        sector = response.meta.get('sector')
        address = response.meta.get('address')
        
        links = response.xpath('//a/@href').extract()
        for link in links:
            if 'contact' in link:
                link = response.urljoin(link)
                yield scrapy.Request(link,callback=self.parse_contact,
                meta={'link':link, 'name':name,'sector':sector,'address':address})

    def parse_contact(self,response):
        name = response.meta.get('name')
        link = response.meta.get('link')
        sector = response.meta.get('sector')
        address = response.meta.get('address')

        text = str(response.text)
        pat = re.compile(r'(?<=>)([\\\d\s()+-]+\d\s?)(?=<)')
        pat2 = re.compile(r'\w+@\w+\.\w+')

        mobile = map(str.strip,re.findall(pat,text))
        email = re.findall(pat2,text)

        yield{
            'Company': name,
            'Sector':sector,
            'Address':address,
            'Contact' : list(set(mobile)),
            'Email' : list(set(email)),
            'Link' : link
        }
