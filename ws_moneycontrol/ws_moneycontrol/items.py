# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WsMoneycontrolItem(scrapy.Item):
    # define the fields for your item here like:
    pass

class StockMarketItem(scrapy.Item):
    company = scrapy.Field()
    ltp = scrapy.Field()
    change_percent = scrapy.Field()
    volume = scrapy.Field()
    buy_price = scrapy.Field()
    sell_price = scrapy.Field()
    buy_qty = scrapy.Field()
    sell_qty = scrapy.Field()
