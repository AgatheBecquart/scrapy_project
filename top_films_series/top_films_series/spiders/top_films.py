import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import TopFilmsSeriesItem


        
class TopFilmsSpider(scrapy.Spider):
    name = "top_films"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["http://www.imdb.com/"]

    def parse(self, response):
        pass


# class MySpider(scrapy.Spider):
#     name = 'my_spider'
#     start_urls = ['http://www.example.com']

#     def parse(self, response):
#         user_agent = response.request.headers['User-Agent']
#         print(f'User agent: {user_agent}')



class Quotespider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/"]
    
    def parse(self, response):
        items = ScraptutoItem()
        all_div_quotes = response.css('div.quote')
        
        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()
            items['title'] = title
            items['author'] = author
            items['tag'] = tag
            yield items

class ScraptutoItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
