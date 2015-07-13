# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from stack.items import StackItem, UserItem
class MongoDBPipeline(object):    
    
    def __init__(self):
        connection = pymongo.Connection(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collection_user = db[settings['MONGODB_COLLECTION_USER']]

    def process_user(self, item, spider):            
        # search for user with the same id then expand data to it user field
        # or simply create a new collection and adding to it
        for data in item:
            if not data:
                raise DropItem("Missing data")
            #self.collection.update({'user_id': item['user_id']}, dict(item), upsert=True)
            self.collection_user.insert(dict(item))
            log.msg("User added to MongoDB database!",
                    level=log.DEBUG)
            return item    
    
    def process_search_index(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data")
            self.collection.update({'user_id': item['user_id']}, dict(item), upsert=True)
            #self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
            return item                    
    
        
    def process_item(self, item, spider):
        #if isinstance(item, UserItem):            
            #return self.process_user(item, spider)        
        #elif isinstance(item, StackItem):
        return self.process_search_index(item, spider)