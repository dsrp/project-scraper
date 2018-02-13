# -*- coding: utf-8 -*-
import scrapy

from .utils import to_fieldname


class GenSpider(scrapy.spiders.SitemapSpider):
    name = 'gen'
    allowed_domains = ['ecovillage.org']

    sitemap_urls = [
        'https://ecovillage.org/gen_project-sitemap1.xml',
        'https://ecovillage.org/gen_project-sitemap2.xml'
    ]

    def parse_meta(self, wrapper):
        """ Parse metadata from header. """

        fields = {}
        for el in wrapper.css('div.gen-project-entry-meta > div > span'):
            name = to_fieldname(el.css('h4::text').extract_first())
            value = el.xpath('./descendant-or-self::text()[position() > 1]').re_first(':*\s*(.*)\s*')

            fields[name] = value

        # TODO: planned_start, other_languages

        return fields

    def parse_sidebar(self, wrapper):
        # TODO: email, social media, keywords, affiliated to, region, country,
        # address, website, coordinates?
        return {}

    def parse(self, response):
        w = response.css('article.gen_project')

        fields = {
            'title': w.css('span.entry-title-primary::text').extract_first(),
            'subtitle': w.css('span.entry-subtitle::text').extract_first(),
            'description': ''.join(w.css('div.project-description > *').extract())
        }

        fields.update(self.parse_meta(w))
        fields.update(self.parse_sidebar(w))

        yield fields
