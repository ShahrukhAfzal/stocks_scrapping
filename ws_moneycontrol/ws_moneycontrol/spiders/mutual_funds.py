import scrapy
from datetime import datetime

class MutualFundSpider(scrapy.Spider):
    name = 'mutual_fund'
    start_urls = ['https://www.moneycontrol.com/mutualfundindia/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'ws_moneycontrol.pipelines.TopPerformingFundsPipeline': 203
        }
    }

    def parse(self, response, **kwargs):
        equity_tables = response.xpath('//section[@class="perform_tbl"]//*[@id="tbequity"]//table')
        for table in equity_tables:
            for row in table.xpath("//tbody/tr"):
                data = row.xpath('td//text()').extract()
                if len(data) > 9: #unneccessary tables
                    break
                data_dict = {
                    'url': row.xpath('td//a/@href').extract_first(),
                    'name': data[0],
                    'crisil_rank': data[1],
                    'aum_cr': data[2],
                    'one_month': data[3],
                    'six_month': data[4],
                    'one_year': data[5],
                    'three_year': data[6],
                    'five_year': data[7],
                }
                yield data_dict

