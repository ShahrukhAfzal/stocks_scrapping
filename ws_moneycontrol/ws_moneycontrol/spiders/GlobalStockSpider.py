import scrapy
from datetime import datetime

class StockMarketSpider(scrapy.Spider):
    name = 'global_stocks'
    start_urls = ['https://www.moneycontrol.com/markets/global-indices/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'ws_moneycontrol.pipelines.GlobalStockMarketPipeline': 201
        }
    }

    @staticmethod
    def strip_text(string, index=-1):
        return string.split('\n')[index].strip()

    def parse(self, response, **kwargs):
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
