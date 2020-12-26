import scrapy
from datetime import datetime

class StockMarketSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = [
        'https://www.moneycontrol.com/markets/indian-indices/'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'ws_moneycontrol.pipelines.StockMarketPipeline': 200
        }
    }

    def parse(self, response, **kwargs):
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

        url = 'https://www.moneycontrol.com/markets/indian-indices/'
        yield response.follow(url, callback=self.get_all_live_market)


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

    def get_all_live_market(self, response):
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