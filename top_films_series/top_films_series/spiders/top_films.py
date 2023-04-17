import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# class CrawlerBooksSpider(CrawlSpider):
#     name = 'crawler_books'
#     allowed_domains = ['imdb.com']

#     user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

#     def start_requests(self):
#         yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
#             'User-Agent': self.user_agent
#         })
        
# class TopFilmsSpider(scrapy.Spider):
#     name = "top_films"
#     allowed_domains = ["www.imdb.com"]
#     start_urls = ["http://www.imdb.com/"]

#     def parse(self, response):
#         pass


class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['http://www.example.com']

    def parse(self, response):
        user_agent = response.request.headers['User-Agent']
        print(f'User agent: {user_agent}')