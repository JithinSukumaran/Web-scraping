import scrapy
from scrapy import Request
import re
from scrapy.exceptions import CloseSpider
import pandas as pd

class PotatoSpider(scrapy.Spider):
    name = 'potato2'
    start_urls = ['https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=24&Tx_State=UP&Tx_District=1&Tx_Market=0&DateFrom=01-Jan-2020&DateTo=31-Dec-2020&Fr_Date=01-Jan-2020&To_Date=31-Dec-2020&Tx_Trend=0&Tx_CommodityHead=Potato&Tx_StateHead=Uttar+Pradesh&Tx_DistrictHead=Agra&Tx_MarketHead=--Select--']
    data = []
    num = 0

    headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'agmarknet.gov.in',
    'Origin': 'https://agmarknet.gov.in',
    'Pragma': 'no-cache',
    'Referer': 'https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=24&Tx_State=UP&Tx_District=1&Tx_Market=0&DateFrom=01-Jan-2020&DateTo=31-Dec-2020&Fr_Date=01-Jan-2020&To_Date=31-Dec-2020&Tx_Trend=0&Tx_CommodityHead=Potato&Tx_StateHead=Uttar+Pradesh&Tx_DistrictHead=Agra&Tx_MarketHead=--Select--',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest'
    }

    def parse(self, response):

        yield scrapy.FormRequest(
                    response.url,
                    callback=self.parse_results,
        )

    def parse_results(self, response):

        pat = re.compile(r'(?<=__VIEWSTATE\|)[\w\d!@#$%^&*()_+/=]+')
        mat = re.findall(pat,response.text)
        try:
            mat = mat[0]
        except:
            pass
        form1={
                'ctl00$ScriptManager1': 'ctl00$cphBody$UpdatePanel1|ctl00$cphBody$GridPriceData',
                'ctl00$ddlLanguages': 'en',
                'ctl00$ddlArrivalPrice': '0',
                'ctl00$ddlCommodity': '24',
                'ctl00$ddlState': 'UP',
                'ctl00$ddlDistrict': '1',
                'ctl00$ddlMarket': '0',
                'ctl00$txtDate': '01-Jan-2020',
                'ctl00$ValidatorExtender1_ClientState':'',
                'ctl00$txtDateTo': '31-Dec-2020',
                'ctl00$ValidatorCalloutExtender2_ClientState': '',
                'ctl00$cphBody$DDLPirceMearure': '0',
                'ctl00$cphBody$DDlExpression': '0',
                'ctl00$cphBody$Textserach': '',
                'ctl00$cphBody$ddlCommodity': '24',
                'ctl00$cphBody$ddlfromyear': '2017',
                'ctl00$cphBody$ddltoyear': '2017',
                'ctl00$cphBody$DropDownDisplay': '0',
                '__EVENTTARGET': 'ctl00$cphBody$GridPriceData',
                '__EVENTARGUMENT': 'Page$Next',
                'ctl00$cphBody$DropDownDisplay': '0',
                '__VIEWSTATE' :response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract_first() if self.num ==0 else mat,
                '__VIEWSTATEGENERATOR': 'B5EE7E14',
                '__VIEWSTATEENCRYPTED': '',
                '__ASYNCPOST': 'true'
            }
        
        for x in range(2,52):
            District_Name = response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[2]/span/text()').extract_first()
            Market_Name= response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[3]/span/text()').extract_first()
            Commodity= response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[4]/span/text()').extract_first()
            Variety= response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[5]/span/text()').extract_first()
            Grade= response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[6]/span/text()').extract_first()
            Min_Price= response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[7]/span/text()').extract_first()
            Max_Price= response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[8]/span/text()').extract_first()
            Modal_Price = response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[9]/span/text()').extract_first()
            Price_Date= response.xpath(f'//*[@id="cphBody_GridPriceData"]/tr[{x}]/td[10]/span/text()').extract_first()           
            
            self.data.append([District_Name,Market_Name,Commodity,Variety,Grade,Min_Price,Max_Price,Modal_Price,Price_Date])

        self.num+=1

        if 'images/Next.png' in response.text:
            yield scrapy.FormRequest(
                        response.url,
                        formdata = form1,
                        callback=self.parse_results,
            )  
        else:
            pd.DataFrame(self.data,columns=['District_Name','Market_Name','Commodity','Variety','Grade','Min_Price','Max_Price','Modal_Price','Price_Date']).to_csv('results.csv')
            raise CloseSpider('bandwidth_exceeded')