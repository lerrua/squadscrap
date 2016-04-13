# -*- coding: utf-8 -*-

import scrapy


class InstagramGrowthItem(scrapy.Item):
    date = scrapy.Field()
    user = scrapy.Field()
    followers = scrapy.Field()
    medias = scrapy.Field()
