import scrapy
from datetime import datetime

class StockMarketSpider(scrapy.Spider):
    name = 'stocks'
    indian_stocks_urls = ['https://www.moneycontrol.com/markets/indian-indices/']
    global_stocks_urls = ['https://www.moneycontrol.com/markets/global-indices/']

    def start_requests(self):
        for url in self.indian_stocks_urls:
            yield scrapy.Request(url, callback=self.parse_1)

        for url in self.global_stocks_urls:
            yield scrapy.Request(url, callback=self.parse_2)

    custom_settings = {
        'ITEM_PIPELINES': {
            'ws_moneycontrol.pipelines.StockMarketPipeline': 200
        }
    }

    @staticmethod
    def strip_text(string, index=-1):
        return string.split('\n')[index].strip()

    def parse_2(self, response, **kwargs):
        data = response.xpath('//*[@class="mctable1 n18_res_table responsive tbl_scroll_resp"]//tbody//tr')
        current_market = ""
        for each in data:
            data = each.xpath('td//text()').extract()
            if len(data) < 11:
                current_market = data[0]
            else:
                data_dict = {
                    "name": self.strip_text(data[0]),
                    "date": data[1],
                    "current_value": data[2],
                    "change": data[3],
                    "percent_change": data[6],
                    "open": self.strip_text(data[9], index=0),
                    "prev_close": data[10],
                    "high": self.strip_text(data[11], index=0),
                    "low": data[12],
                    "market": current_market,
                    'entity': 'global_market'
                }

                yield data_dict

    def parse_1(self, response, **kwargs):
        self.current_time = datetime.now()
        return self.parse_pages(response)

    def parse_pages(self, response):
        #Bombay Stock Exchange
        bse_all_pages = response.xpath('//*[(@id = "collapse1")]/*[@class="accordion_list"]/li/a/@href').extract()
        for url in bse_all_pages:
            try:
                yield response.follow(url, callback=self.get_all_bse)
            except:
                pass

        nse_all_pages = response.xpath('//*[(@id = "collapse2")]/*[@class="accordion_list"]/li/a/@href').extract()
        for url in nse_all_pages:
            try:
                yield response.follow(url, callback=self.get_all_nse)
            except:
                pass

    def get_all_bse(self, response):
        table = response.xpath('//*[(@id = "nsebse_1")]//*[@class="responsive"]//tbody//tr')
        for row in table:
            data = row.xpath('td//text()').extract()
            data_dict = {
                'url': row.xpath('td//a/@href').extract_first(),
                'company': data[0],
                'ltp': data[1],
                'change_percent': data[2],
                'volume': data[3],
                'buy_price': data[4],
                'sell_price': data[5],
                'buy_qty': data[6],
                'sell_qty': data[7],
                'market': "Bombay Stock Exchange",
                'entity': 'stock',
                'updated_on': self.current_time,
            }
            yield data_dict

    def get_all_nse(self, response):
        table = response.xpath('//*[(@id = "nsebse_1")]//*[@class="responsive"]//tbody//tr')
        for row in table:
            data = row.xpath('td//text()').extract()
            data_dict = {
                'url': row.xpath('td//a/@href').extract_first(),
                'company': data[0],
                'ltp': data[1],
                'change_percent': data[2],
                'volume': data[3],
                'buy_price': data[4],
                'sell_price': data[5],
                'buy_qty': data[6],
                'sell_qty': data[7],
                'market': "National Stock Exchange",
                'entity': 'stock',
                'updated_on': self.current_time,
            }
            yield data_dict

		#Live Bombay Stock Exchange
        table = response.xpath('//*[(@id = "nsebse_3")]//*[@class="responsive"]/tbody/tr')
        for row in table:
            data = row.xpath('td//text()').extract()
            data_dict = {
                'url': row.xpath('td//a/@href').extract_first(),
                'name': data[0],
                'current_value': data[1],
                'change': data[2],
                'percent_change': data[3],
                'open': data[4],
                'high': data[5],
                'low': data[6],
                'market': 'Bombay Stock Exchange',
                'entity': 'live_market',
                'updated_on': self.current_time,
            }
            yield data_dict

        #Live National Stock Exchange
        table = response.xpath('//*[(@id = "nsebse_4")]//*[@class="responsive"]/tbody/tr')
        for row in table:
            data = row.xpath('td//text()').extract()
            data_dict = {
                'url': row.xpath('td//a/@href').extract_first(),
                'name': data[0],
                'current_value': data[1],
                'change': data[2],
                'percent_change': data[3],
                'open': data[4],
                'high': data[5],
                'low': data[6],
                'market': 'National Stock Exchange',
                'entity': 'live_market',
                'updated_on': self.current_time,
            }
            yield data_dict