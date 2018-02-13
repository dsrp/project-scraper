# -*- coding: utf-8 -*-
import scrapy


def to_fieldname(s):
    """ Cleanup string to use for JSON fieldname. """

    import re

    return re.sub(r'\W+', '', s.replace(' ', '_')).lower()


def key_value_from_b(el):
    """ Return key, value from <b>Key:</b> value. """

    raw_key = el.css('b::text').re_first('(.*):')

    if raw_key:
        key = to_fieldname(raw_key)
    else:
        raise Exception('No raw key found.')

    raw_value = el.xpath('./descendant-or-self::text()[position() > 1]')

    if raw_value:
        value = ''.join(raw_value.extract()).strip()
        return key, value
    else:
        raise Exception('No raw value found.')


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
            try:
                key, value = key_value_from_b(field)
            except Exception as e:
                self.logger.exception(e)
                continue

            fields[key] = value

        return fields

    def parse_rest(self, main):
        """ Parse remainging (lower) fields. """

        rest = main.css('.listing-info-blocks')
        fields = {}
        for field in rest.css('ul > li'):
            try:
                key, value = key_value_from_b(field)
            except Exception as e:
                self.logger.exception(e)
                continue

            fields[key] = value

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
        fields.update(self.parse_rest(main))

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
