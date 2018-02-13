# -*- coding: utf-8 -*-
import scrapy


class GenSpider(scrapy.spiders.SitemapSpider):
    name = 'gen'
    allowed_domains = ['ecovillage.org']

    sitemap_urls = [
        'https://ecovillage.org/gen_project-sitemap1.xml',
        'https://ecovillage.org/gen_project-sitemap2.xml'
    ]

    def parse(self, response):
        pass
