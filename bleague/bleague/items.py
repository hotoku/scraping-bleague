# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BleagueItem(scrapy.Item):
    year = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    start_time = scrapy.Field()
    home = scrapy.Field()
    away = scrapy.Field()
    arena = scrapy.Field()
