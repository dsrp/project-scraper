# -*- coding: utf-8 -*-
import scrapy


class FicSpider(scrapy.spiders.SitemapSpider):
    name = 'fic'
    allowed_domains = ['ic.org']

    sitemap_urls = [
        'https://www.ic.org/directory-sitemap1.xml',
        'https://www.ic.org/directory-sitemap2.xml'
    ]

    def parse_sidebar(self, main):
        sidebar = main.css('div.row.mb-2 > div.col-sm-10')

        return {
            'status': self.side_field(sidebar, 'Status'),
            'started_planning': self.side_field(sidebar, 'Started Planning'),
            'started_living': self.side_field(sidebar, 'Start Living Together'),
            'visitors_accepted': self.side_field(sidebar, 'Visitors accepted'),
            'new_members': self.side_field(sidebar, 'Open to new Members'),
            'contact_name': self.side_field(sidebar, 'Contact Name'),
            'facebook': self.side_field(sidebar, 'Facebook'),
            'other_social': self.side_field(sidebar, 'Other social'),
            'address': self.side_field(sidebar, 'Community Address'),
        }

    def parse_main(self, main):
        return {
            'title': main.css('h1::text').extract_first(),
            'description': self.main_text(main, 'Community Description'),
            'mission': self.main_text(main, 'Mission Statement'),

        }

    def parse(self, response):
        main = response.css('div.directory-listing')
        fields = self.parse_main(main)

        fields.update(self.parse_sidebar(main))

        yield fields

    def side_field(self, el, fieldname):
        """ Extracts fields from the right side. """
        xpath = '*//li[b[text() = "{}:"]]/descendant-or-self::text()[position() > 1]'
        xpath = xpath.format(fieldname)

        result = el.xpath(xpath).extract()

        if result:
            return ''.join(result).strip()

    def main_text(self, el, header):
        """ Parse main header (h2) content, keeping HTML """
        xpath = '//p[preceding::h2[text()="{}"]]'.format(header)

        text_nodes = el.xpath(xpath).extract()

        return '\n'.join(text_nodes).strip()
