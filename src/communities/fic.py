from scrapy.spiders import SitemapSpider


class FicSpider(SitemapSpider):
    sitemap_urls = [
        'https://www.ic.org/directory-sitemap1.xml',
        'https://www.ic.org/directory-sitemap2.xml'
    ]

    def parse(self, response):
        pass # ... scrape item here ...
