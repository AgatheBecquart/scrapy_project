import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class TopSeriesSpider(CrawlSpider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'top_films_series.pipelines.TopSeriesPipeline': 400
        }
    }
    name = 'crawler_series'
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
        item['episode_duration'] = response.css(".ipc-inline-list--show-dividers li:nth-of-type(4)::text").extract_first()
        #item['num_seasons'] = response.css("[data-testid='hero-title-block__metadata'] span[data-testid='TitleEpisodeCount']::text").extract_first()
        item['num_episodes'] = response.css('[data-testid="episodes-header"] span.ipc-title__subtext::text').extract_first()
        item['affiche'] = response.css('div.ipc-media--poster-l img.ipc-image::attr(src)').extract_first()
        
        # Calcul de la durée totale
        episode_duration = item.get('episode_duration')
        num_episodes = item.get('num_episodes')
        total_duration = None
        if episode_duration and num_episodes:
            if 'h' in episode_duration:
                if 'm' in episode_duration:
                    # La durée de l'épisode est de la forme 'Xh Ymin'
                    hours, minutes = episode_duration.split('h')
                    total_duration = int(hours) * 60 + int(minutes.strip('min'))
                elif int(episode_duration.strip('h')) >= 2:
                    # La durée de l'épisode est supérieure ou égale à 2 heures, on l'affecte directement à la durée totale
                    hours, minutes = episode_duration.split('h')
                    total_duration = int(hours) * 60
                    if 'm' in minutes:
                        total_duration += int(minutes.strip('min'))
                else:
                    # La durée de l'épisode est comprise entre 1 et 2 heures, on la convertit en minutes
                    total_duration = int(episode_duration.strip('h')) * 60
            else:
                # La durée de l'épisode est de la forme 'Xmin'
                total_duration = int(episode_duration.strip('min'))
                total_duration *= int(num_episodes)
            item['total_duration'] = total_duration

        item['total_duration'] = total_duration

        yield item
        