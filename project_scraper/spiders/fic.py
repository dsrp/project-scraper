# -*- coding: utf-8 -*-
import scrapy


class FicSpider(scrapy.spiders.SitemapSpider):
    name = 'fic'
    allowed_domains = ['ic.org']

    sitemap_urls = [
        'https://www.ic.org/directory-sitemap1.xml',
        'https://www.ic.org/directory-sitemap2.xml'
    ]

    def parse(self, response):
        pass
