# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo


class StockMarketPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['stock']
        self.stocks_tb = db['stocks_tb']
        self.live_market_tb = db['live_market_tb']
        self.global_market_tb = db['global_market_tb']

    def process_item(self, item, spider):
        entity = item.pop('entity')
        if entity == 'stock':
            self.stocks_tb.insert(item)
        elif entity == 'live_market':
            self.live_market_tb.insert(item)
        elif entity == 'global_market':
            self.global_market_tb.insert(item)

        return item
