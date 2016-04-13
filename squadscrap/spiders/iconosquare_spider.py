# -*- coding: utf-8 -*-

import datetime

from scrapy import Spider
from scrapy.selector import Selector

from . import ACCOUNTS
from squadscrap.items import InstagramGrowthItem


class IconosquareSpider(Spider):
    name = "iconosquare"
    allowed_domains = ["iconosquare.com"]
    start_urls = [
        "http://iconosquare.com/{}".format(a) for a in ACCOUNTS
    ]

    def parse(self, response):
        item = InstagramGrowthItem()
        item['date'] = datetime.datetime.now()
        item['user'] = Selector(response).xpath(
            '//*[@id="userProfilLarge"]/div[1]/div[2]/div/h2/text()').extract()[0]
        item['followers'] = Selector(response).xpath(
            '//*[@id="userProfilLarge"]/div[2]/a[2]/span[1]/text()').extract()[0]
        item['medias'] = Selector(response).xpath(
            '//*[@id="userProfilLarge"]/div[2]/span/span[1]/text()').extract()[0]
        return item
