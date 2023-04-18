# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo 
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')

class TopSeriesPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(
            ATLAS_KEY,
        )
        db = self.conn['Top250']
        self.collection = db['Top_series']
        
    def process_item(self, item, spider):
        self.collection.insert_one(item)
        return item
    
class TopFilmsPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(
            ATLAS_KEY,
        )
        db = self.conn['Top250']
        self.collection = db['Top_films']
        
    def process_item(self, item, spider):
        self.collection.insert_one(item)
        return item

