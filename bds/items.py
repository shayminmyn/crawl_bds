# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

class BdsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    square = scrapy.Field()
    address = scrapy.Field()
    category = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    dateCreate = scrapy.Field()
