import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# from fake_useragent import UserAgent
def convert_to_minutes(duration):
    duration_str = ''.join(duration)  # Combine toutes les chaînes de la liste en une seule
    parts = duration_str.split()  # Sépare les parties de la durée par des espaces
    hours = 0
    minutes = 0
    for part in parts:
        if part.endswith('h'):  # Si la partie se termine par 'h', c'est le nombre d'heures
            hours = int(part[:-1])
        elif part.endswith('m'):  # Si la partie se termine par 'm', c'est le nombre de minutes
            minutes = int(part[:-1])
    return hours*60 + minutes




class TopfilmsspiderSpider(CrawlSpider):
    name = 'crawler_films'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

    rules = (
    Rule(LinkExtractor(restrict_css='.titleColumn a'), callback='parse_item'),
    )


    
    def parse_item(self, response):
        item = {}
        
        item['titre'] = response.css('span.sc-afe43def-1.fDTGTb::text').extract()
        item['titre original'] = response.css('div.sc-afe43def-3::text').extract()
        item['year'] = response.css('.ipc-inline-list__item a[href*="releaseinfo"]::text')[0].extract()
        item['note']=response.css('.sc-52d569c6-1 span.sc-bde20123-1::text').extract()
        item['genre'] = response.css('div.ipc-chip-list__scroller ::text').extract()
        item['duree']=convert_to_minutes(response.css('.sc-afe43def-4 li:nth-of-type(3) ::text').extract())
        item['synopsis']=response.css('span.sc-5f699a2-2 ::text').extract()
        item['casting']=response.css('.sc-52d569c6-3 .ipc-metadata-list-item--link div ::text').extract()
        item['pays']=response.css   ("[data-testid='title-details-origin'] a::text").extract()
        item['public']=response.css('.sc-afe43def-4 li:nth-of-type(2) a::text').extract()     
        
        return item
       





