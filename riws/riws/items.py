# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PazBookItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    editorial = scrapy.Field()
    edition_date = scrapy.Field()
    category = scrapy.Field()
    isbn = scrapy.Field()
    pages = scrapy.Field()
    synopsis = scrapy.Field()
    cover = scrapy.Field()
    cost = scrapy.Field()