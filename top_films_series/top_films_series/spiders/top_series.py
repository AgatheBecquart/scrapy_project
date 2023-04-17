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
        item['original_title'] = response.css('div.sc-afe43def-3::text').extract()
        item['score'] = response.css('span.sc-bde20123-1.iZlgcd::text')[0].extract()
        item['genre'] = response.css('a span.ipc-chip__text::text').extract()
        item['year'] = response.css('.ipc-inline-list__item a[href*="releaseinfo"]::text')[0].extract()
        # item['duration'] = response.xpath('//div[contains(text(), "Runtime")]/following-sibling::text()').get().strip()
        item['description'] = response.css('span.sc-5f699a2-2::text').extract()
        item['cast'] = response.css('.sc-52d569c6-3 a.ipc-metadata-list-item__list-content-item::text').extract()
        item['public'] = response.css('.sc-afe43def-4 li:nth-of-type(3) a::text').extract()
        item['country'] = response.css("[data-testid='title-details-origin'] a::text").extract()
        item['language'] = response.css("[data-testid='title-details-languages'] a::text").extract()
        #item['num_seasons'] = response.css("[data-testid='hero-title-block__metadata'] span[data-testid='TitleEpisodeCount']::text").extract_first()
        #item['num_episodes'] = response.css("[data-testid='season-episodes'] .ipc-button__text::text").extract()
        yield item