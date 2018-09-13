# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LvyouItem(scrapy.Item):
    # define the fields for your item here like:
    remark_acccount = scrapy.Field()
    source = scrapy.Field()
    scene_name = scrapy.Field()
    remark = scrapy.Field()
    time = scrapy.Field()
    star = scrapy.Field()
