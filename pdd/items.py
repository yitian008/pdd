# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PddItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    share_url = scrapy.Field()
    share_user = scrapy.Field()
    share_user_bd_id = scrapy.Field()
    share_time = scrapy.Field()
    file_size = scrapy.Field()
    file_class = scrapy.Field()
    ford = scrapy.Field()

