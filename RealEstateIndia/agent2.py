import scrapy
import json
from scrapy import Request
import re
import bs4

class Agent2Spider(scrapy.Spider):
    name = 'agent2'
    ls = []
    def start_requests(self):
        url = 'https://www.realestateindia.com/Functions/fetch_service_classified_results.php'
        for _ in range(10):  # no of time you want to go through the site
            for x in range(82):  # no. of pages in the site

           # for Gurgaon
                form = {
                    'pageno': str(x),
                    'city_level': '2',
                    'cat_id': '116',
                    'city_id': '899',
                    'file_name': 'vadodara',
                    'ref_state_file_name': 'gujarat',
                    'ref_city_file_name': 'vadodara',
                    'solr_rand_no': '750287062',
                    'location': 'https://www.realestateindia.com/agents-brokers-in-vadodara.htm'
                    } 

        #    # for Ahmedabad
        #         form = {
        #             'pageno': str(x),
        #             'city_level': '2',
        #             'cat_id': '116',
        #             'city_id': '700',
        #             'file_name': 'ahmedabad',
        #             'ref_state_file_name': 'gujarat',
        #             'ref_city_file_name': 'ahmedabad',
        #             'solr_rand_no': '1704217146',
        #             'location': 'https://www.realestateindia.com/agents-brokers-in-ahmedabad.htm'
        #             } 

                # # for Chennai
                # form = {
                #     'pageno': str(x),
                #     'city_level': '2',
                #     'cat_id': '116',
                #     'city_id': '3187',
                #     'file_name': 'chennai',
                #     'ref_state_file_name': 'tamilnadu',
                #     'ref_city_file_name': 'chennai',
                #     'solr_rand_no': '1751714164',
                #     'location': 'https://www.realestateindia.com/agents-brokers-in-chennai.htm'
                #     } 

                # # for Bangalore
                # form = {
                #     'pageno': str(x),
                #     'city_level': '2',
                #     'cat_id': '116',
                #     'city_id': '1317',
                #     'file_name': 'bangalore',
                #     'ref_state_file_name': 'karnataka',
                #     'ref_city_file_name': 'bangalore',
                #     'solr_rand_no': '97966453',
                #     'location': 'https://www.realestateindia.com/agents-brokers-in-bangalore.htm'
                #     } 

                # for jaipur
                # form = {
                #     'pageno': str(x),
                #     'city_level': '2',
                #     'cat_id': '116',
                #     'city_id': '2934',
                #     'file_name': 'jaipur',
                #     'ref_state_file_name': 'rajasthan',
                #     'ref_city_file_name': 'jaipur',
                #     'solr_rand_no': '1268327717',
                #     'location': 'https://www.realestateindia.com/agents-brokers-in-jaipur.htm'
                #     } 

                # # for Delhi
                # form = {
                #     'pageno': str(x),
                #     'city_level': '2',
                #     'cat_id': '116',
                #     'city_id': '584',
                #     'file_name': 'delhi',
                #     'ref_state_file_name': 'delhi',
                #     'ref_city_file_name': 'delhi',
                #     'solr_rand_no': '406877215',
                #     'location': 'https://www.realestateindia.com/agents-brokers-in-delhi.htm'
                #     } 

                # # for mumbai
                # form = {
                #     'pageno': str(x),
                #     'city_level': '2',
                #     'cat_id': '116',
                #     'city_id': '2298',
                #     'file_name': 'mumbai',
                #     'ref_state_file_name': 'maharashtra',
                #     'ref_city_file_name': 'mumbai',
                #     'solr_rand_no': '1790712745',
                #     'location': 'https://www.realestateindia.com/agents-brokers-in-mumbai.htm'
                #     } 

            
                # # for ahmedabad
                # form = {
                #     'pageno': str(x),
                #     'city_level': '2',
                #     'cat_id': '116',
                #     'city_id': '700',
                #     'file_name': 'ahmedabad',
                #     'ref_state_file_name': 'gujarat',
                #     'ref_city_file_name': 'ahmedabad',
                #     'solr_rand_no': '599484666',
                #     'location': 'https://www.realestateindia.com/agents-brokers-in-ahmedabad.htm'
                #     } 


                yield scrapy.FormRequest(
                url,
                formdata = form,
                callback=self.parse,
                )  

    def parse(self, response):

        resp = response.text
        # print(resp)
        soup = bs4.BeautifulSoup(resp,'lxml')

        # print(soup.select('article')[0])

        # print('='*100)
        # print(type(soup.select('article')))
        # print('='*100)

        for x in soup.select('article'):
            url = 'https://www.realestateindia.com/view_enquiry_now.php?sid=0.7585429088537894'

            # name and address of the agency
            name = x.find_all('span',itemprop="name")[0].getText()
            address = x.find_all('span',itemprop="address")[0].getText()
            
            # the localities the agent is active on
            # localities = x.find_all('p',class_="mb12px")[0].getText()

            lpat = re.compile(r'(?<=localities :</span>).*?(?=<)')
            try:
                localities = re.search(lpat,str(x))
                localities = localities.group()
            except:
                localities = ''

            # the number needed to get the contact of agent
            # number = x.find_all('a')
            # mail = re.findall("'([\d]+)'",number[1]['onclick'])[0]

            pat = re.compile(r"(?<='send_class_enq',')\d+")
            # print(type(str(x)))
            # print(str(x))
            # print('='*100)
            mat = re.search(pat,str(x))
            try:
                mail = mat.group()
            except:
                print('='*100)
                print(str(x))
            


# new line added
            if mail in self.ls:
                continue
            else:
                self.ls.append(mail)
            # print(number[1])
            # print(re.findall("'([\d]+)'",number[1]['onclick'])[0])
            # print('='*100)

            form2 = {
                'mailto':mail,
                'id':'send_class_enq_contact',
                'action_type':'send_inquiry',
                'fname':'jithin',
                'user_name':'jithin.suku09@gmail.com',
                'mobile':'8655857686',
                } 


            yield scrapy.FormRequest(
            url,
            formdata = form2,
            callback=self.parse_page,
            meta = {'n': name,
            'a' : address,
            'l':localities,
            'm':mail}
            ) 


    def parse_page(self,response):
        Agency_name = response.meta.get('n')
        Agency_address = response.meta.get('a')
        localities = response.meta.get('l')
        mail = response.meta.get('m')

        res = response.text
        pat = re.compile(r'(?<=<p>)[\b,/\w.\s\d]+(?=</p>)')
        pat1 = re.compile(r'(?<=<p>)[,\s+\d-]+(?=</p>)')

        name = re.search(pat,res)
        number = re.search(pat1,res)

        try:
            name = name.group()
        except:
            name = ''
        try:
            number = number.group()
        except:
            number = 'No number'
            print('='*100)
            print(mail)
            print('='*100)


        yield{
            'Agency Name': Agency_name,
            'Address':Agency_address,
            'Operating Localities':  localities,
            # 'Property Type Deals In': type,
            # 'services offered' : response.xpath('//li[3]/p[2]/text()').extract_first(),
            'Name of Agent': name,
            'Contact Number': number,
            # 'Link': response.url
        }


# proxy pool test

# from scrapy.shell import inspect_response
# import scrapy

# class AgentSpider(scrapy.Spider):
#     name = 'agent2'

#     def start_requests(self):
#         for i in range(5):
#             yield scrapy.Request(url='http://httpbin.org/ip',dont_filter=True)

#     def parse(self,response):
#         print(response.text)

        