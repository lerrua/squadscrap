# -*- coding: utf-8 -*-

from datetime import datetime

import arrow
from scrapy import Spider
from scrapy.http.request import Request
from scrapy.selector import Selector, HtmlXPathSelector

from . import ACCOUNTS
from squadscrap.items import InstagramGrowthItem, InstagramEngagementItem

UTC = arrow.utcnow()

class IconosquareGrowthSpider(Spider):
    name = "growth"
    allowed_domains = ["iconosquare.com"]
    start_urls = [
        "http://iconosquare.com/{}".format(a) for a in ACCOUNTS
    ]

    def parse(self, response):
        item = InstagramGrowthItem()
        item['date'] = UTC.to('America/Sao_Paulo').format('YYYY-MM-DD')
        item['user'] = Selector(response).xpath(
            '//*[@id="userProfilLarge"]/div[1]/div[2]/div/h2/text()').extract()[0]
        item['followers'] = Selector(response).xpath(
            '//*[@id="userProfilLarge"]/div[2]/a[2]/span[1]/text()').extract()[0]
        item['medias'] = Selector(response).xpath(
            '//*[@id="userProfilLarge"]/div[2]/span/span[1]/text()').extract()[0]
        return item


class IconosquareEngagementSpider(Spider):
    name = "engagement"
    allowed_domains = ["iconosquare.com"]
    start_urls = [
        "http://iconosquare.com/{}".format(a) for a in ACCOUNTS
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        next_page = hxs.select('//a[@class="more"][1]/@href').extract()

        item = InstagramEngagementItem()

        photos_link = Selector(response).xpath(
            '//*[@class="photos-wrapper"]/div[1]/a/@href').extract()

        if not not next_page:
            yield Request(next_page[0], self.parse)

        for link in photos_link:
            if link.startswith(u'http://iconosquare.com'):
                request = Request(link, callback=self.parse_link)
                request.meta['item'] = item
                yield request

    def parse_link(self, response):
        item = response.meta['item']

        item['user'] = response.xpath(
            '//a[@class="list-username-user"]/text()').extract()
        item['likes'] = response.xpath(
            '//span[@class="nb_like_score"]/text()').extract()
        item['comments'] = response.xpath(
            '//span[@class="nb_comment_score"]/text()').extract()
        created = response.xpath(
            '//*[@id="conteneurLoad"]/div/div[1]/div[1]/p[2]/span/text()').extract()
        item['date'] = arrow.get(created[0]).replace(hours=-3).format('YYYY-MM-DD')

        return item
