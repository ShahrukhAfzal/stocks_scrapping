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
        self.bombay_stocks_tb = db['bombay_stocks_tb']
        self.national_stocks_tb = db['national_stocks_tb']

    def process_item(self, item, spider):
        if 'bombay' in item.get('market').lower():
            self.bombay_stocks_tb.insert(item)
        elif 'national' in item.get('market').lower():
            self.national_stocks_tb.insert(item)
        return item
