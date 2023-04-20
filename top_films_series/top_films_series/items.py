# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TopSeriesItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    score = scrapy.Field()
    genre = scrapy.Field()
    year = scrapy.Field()
    description = scrapy.Field()
    cast = scrapy.Field()
    public = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    episode_duration = scrapy.Field()
    num_episodes = scrapy.Field()
    affiche = scrapy.Field()
    total_duration = scrapy.Field()
    
class TopFilmsItem(scrapy.Item):
    titre = scrapy.Field()
    titre_original = scrapy.Field()
    year = scrapy.Field()
    note = scrapy.Field()
    genre = scrapy.Field()
    duree = scrapy.Field()
    synopsis = scrapy.Field()
    casting = scrapy.Field()
    pays = scrapy.Field()
    public = scrapy.Field()
    affiche = scrapy.Field()

