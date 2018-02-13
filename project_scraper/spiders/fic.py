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
        main = response.css('#main')

        yield {
            'title': main.css('h1::text').extract_first(),
            'description': self.parse_main_text(main, 'Community Description'),
            'mission': self.parse_main_text(main, 'Mission Statement'),
            'status': self.parse_side_field(main, 'Status')

        }

    def parse_side_field(self, main, fieldname):
        """ Extracts fields from the right side. """
        xpath = '//ul/li/text()[preceding::b[text()="{0}:"]]'.format(fieldname)
        return main.xpath(xpath).extract_first().strip()

    def parse_main_text(self, main, header):
        """ Parse main header (h2) content, keeping HTML """
        xpath = '//p[preceding::h2[text()="{0}"]]'.format(header)

        text_nodes = main.xpath(xpath).extract()

        return '\n'.join(text_nodes).strip()
