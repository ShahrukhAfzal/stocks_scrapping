import scrapy

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
                'company': data[0],
                'ltp': data[1],
                'change_percent': data[2],
                'volume': data[3],
                'buy_price': data[4],
                'sell_price': data[5],
                'buy_qty': data[6],
                'sell_qty': data[7],
                'market': "Bombay Stock Exchange",
                'url': row.xpath('td//a/@href').extract_first()

            }

            yield data_dict

    def get_all_nse(self, response):
        table = response.xpath('//*[(@id = "nsebse_1")]//*[@class="responsive"]//tbody//tr')
        for row in table:
            data = row.xpath('td//text()').extract()
            data_dict = {
                'company': data[0],
                'ltp': data[1],
                'change_percent': data[2],
                'volume': data[3],
                'buy_price': data[4],
                'sell_price': data[5],
                'buy_qty': data[6],
                'sell_qty': data[7],
                'market': "National Stock Exchange",
                'url': row.xpath('td//a/@href').extract_first()
            }

            yield data_dict