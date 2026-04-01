# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PcPartsItem(scrapy.Item):
    part_type = scrapy.Field()
    name = scrapy.Field()
    price_str = scrapy.Field()
    price_num = scrapy.Field()
    currency = scrapy.Field()
    retailer = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    in_stock = scrapy.Field()
