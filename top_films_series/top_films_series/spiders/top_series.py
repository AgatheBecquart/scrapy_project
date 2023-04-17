import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class TopSeriesSpider(CrawlSpider):
    name = 'crawler_books'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', headers={
            'User-Agent': self.user_agent
        })

    rules = (
    Rule(LinkExtractor(restrict_css='.titleColumn a'), callback='parse_item'),
    )


    def parse_item(self, response):
        item = {}
        item['title'] = response.css('span.sc-afe43def-1.fDTGTb::text').extract()
        # item['original_title'] = response.xpath('//div[contains(text(), "Original Title")]/following-sibling::text()').get().strip()
        item['score'] = response.css('span.sc-bde20123-1.iZlgcd::text').extract()
        item['genre'] = response.css('a span.ipc-chip__text::text').extract()
        item['year'] = response.css('.ipc-inline-list__item a[href*="releaseinfo"]::text')[0].extract()
        # item['duration'] = response.xpath('//div[contains(text(), "Runtime")]/following-sibling::text()').get().strip()
        # item['description'] = response.xpath('//div[contains(@class, "SummaryText")]//text()').get()
        # item['cast'] = response.xpath('//h4[contains(text(), "Stars")]/following-sibling::a/text()').getall()
        # item['certificate'] = response.xpath('//div[contains(text(), "Certificate")]/following-sibling::text()').get().strip()
        # item['country'] = response.xpath('//div[contains(text(), "Country")]/following-sibling::a/text()').getall()
        # item['language'] = response.xpath('//div[contains(text(), "Language")]/following-sibling::a/text()').getall()
        yield item