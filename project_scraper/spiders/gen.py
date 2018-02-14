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
            name = to_fieldname(el.css('h4::text').extract_first())
            value = el.xpath(
                './descendant-or-self::text()[position() > 1]'
            ).re_first(':*\s*(.*)\s*')

            fields[name] = value

        # TODO: planned_start, other_languages

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
                value = el.xpath(
                    './descendant-or-self::text()[position() > 1]'
                ).re_first(':*\s*(.*)\s*')

            fields[name] = value

        # TODO: email, social media, keywords, affiliated to, region, country,
        # address, website, coordinates?
        # import ipdb; ipdb.set_trace()
        return fields

    def parse(self, response):
        article = response.css('article.gen_project')

        fields = {
            'title': article.css('span.entry-title-primary::text').extract_first(),
            'subtitle': article.css('span.entry-subtitle::text').extract_first(),
            'description': ''.join(article.css('div.project-description > *').extract())
        }

        fields.update(self.parse_meta(article))
        fields.update(self.parse_sidebar(response))

        yield fields
