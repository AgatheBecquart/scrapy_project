import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlerBooksSpider(CrawlSpider):
    name = 'crawler_books'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', headers={
            'User-Agent': self.user_agent
        })
    
class TopSeriesSpider(scrapy.Spider):
    name = "top_series"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["http://www.imdb.com/"]

    def parse(self, response):
        pass
