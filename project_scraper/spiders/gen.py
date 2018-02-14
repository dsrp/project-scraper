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

    def parse_meta(self, el):
        """ Parse metadata from header. """

        fields = {}
        for el in el.css('div.gen-project-entry-meta > div > span'):
            keys = list(
                map(to_fieldname, el.css('h4 ::text').extract())
            )
            values = el.xpath(
                './h4/following-sibling::text()'
            ).re(':*\s*(.*)\s*')

            # Remove empty values...
            values = [value for value in values if value]

            if len(keys) != len(values):
                self.logger.error(
                    'Number of values (%d) doesn\'t match keys (%d) for %s.',
                    len(values), len(keys), el.extract()
                )

                continue

            fields.update(zip(keys, values))

        return fields

    def parse_sidebar(self, el):
        sidebar = el.css('aside.sidebar-primary')

        fields = {}
        for el in sidebar.css('ul.sidebar-info-list > li'):
            name = to_fieldname(el.css('h4::text').extract_first())

            subvalues = el.css('li li')
            if subvalues:
                # Multi-valued field

                if name.startswith('email'):
                    self.logger.info('Skipping emails (obfuscated)')
                    continue

                # Treat it like links
                keys = subvalues.css('a ::text').extract()
                values = subvalues.css('a::attr("href")').extract()

                if len(keys) != len(values):
                    self.logger.error(
                        'Number of subvalues (%d) for %s doesn\'t match keys (%d).',
                        len(values), name, len(keys)
                    )

                    continue

                value = dict(zip(keys, values))
            else:
                # Single valued
                value = ''.join(el.xpath(
                    './descendant-or-self::text()[position() > 1]'
                ).re(':*\s*(.*)\s*'))

            fields[name] = value

        fields['coordinates'] = sidebar.css(
            'section.sidebar-info-map a::attr("href")'
        ).re_first('/maps/place/(.*)/')

        return fields

    def parse_members_visitors(self, el):
        el = el.css('div.participation-info')

        fields = {}

        visitors_description = ''.join(el.css('p').extract())
        if visitors_description:
            fields['visitors_description'] = visitors_description

        for el in el.css('li ::text'):
            current_members = el.re_first('Current members: (.*)')
            if current_members:
                fields['current_members'] = current_members
            else:
                # Treat like boolean tag
                fields[to_fieldname(el.extract())] = True

        return fields

    def parse_title(self, el):
        subtitle = el.css('span.entry-subtitle ::text').extract_first()
        if subtitle:
            return {
                'title': el.css(
                    'span.entry-title-primary ::text').extract_first(),
                'subtitle': subtitle
            }

        return {
            'title': el.css('h1.entry-title ::text').extract_first()
        }

    def parse(self, response):
        article = response.css('article.gen_project')

        if not article:
            self.logger.info('Skipping %s; not a directory listing.', response)
            return

        fields = {
            'description': ''.join(
                article.css('div.project-description > *').extract()
            )
        }

        fields.update(self.parse_title(article))
        fields.update(self.parse_meta(article))
        fields.update(self.parse_sidebar(response))
        fields.update(self.parse_members_visitors(response))

        yield fields
