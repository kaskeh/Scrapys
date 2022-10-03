import scrapy


class Git1Spider(scrapy.Spider):
    name = 'git1'
    allowed_domains = ['guthub.com']
    start_urls = ['http://guthub.com/']

    def parse(self, response):
        pass
