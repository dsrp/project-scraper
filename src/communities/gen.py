from scrapy.spiders import SitemapSpider


class GenSpider(SitemapSpider):
    sitemap_urls = [
        'https://ecovillage.org/gen_project-sitemap1.xml',
        'https://ecovillage.org/gen_project-sitemap2.xml'
    ]

    def parse(self, response):
        pass # ... scrape item here ...
