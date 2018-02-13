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

        fields = {}
        for field in sidebar.css('li'):
            raw_key = field.css('b::text').re_first('(.*):')

            if raw_key:
                key = raw_key.lower().replace(' ', '_')
            else:
                self.logger.info('No raw key found.')
                continue

            raw_value = field.xpath('./descendant-or-self::text()[position() > 1]')

            if raw_value:
                value = ''.join(raw_value.extract()).strip()
                fields[key] = value
            else:
                self.logger.info('No raw value found.')

        return fields

    def parse_main(self, main):
        return {
            'title': main.css('h1::text').extract_first(),
            'description': self.main_text(main, 'Community Description'),
            'mission': self.main_text(main, 'Mission Statement'),

        }

    def parse(self, response):
        main = response.css('div.directory-listing')
        if not main:
            self.logger.info('Skipping %s; not a directory listing.', response)
            return

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
