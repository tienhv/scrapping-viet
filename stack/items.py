# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class StackItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    gender = Field()
    age = Field()
    image = Field()
    picture = Field()
    location = Field()
    views = Field()
    log_date = Field()
    user_id = Field()
    #user_item = Field() #containing the user-data, below, dict(usser)
    user_url = Field()
      
        
    
class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    ip_date = Field()
    modified_date = Field()
    gender = Field()
    age = Field()
    height = Field()
    weight = Field()
    body = Field()
    city = Field()
    state = Field()
    zip_code = Field()
    country = Field()
    religion = Field()
    education = Field()
    job = Field()
    smoking = Field()
    drinking = Field()
    status = Field()
    goal = Field()
    free_time = Field()
    i_am = Field()
    looking_for = Field()
    user_images = Field() # a list containing all photos of user user_images.append(Item)
    user_id = Field()    
    #con thieu zip va tieu bang nua la xong
    # nhu vay con thieu 2 cai: dia chi, hinh anh

    

    
