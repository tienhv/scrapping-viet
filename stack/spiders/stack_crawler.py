# -*- coding: utf-8 -*-
import scrapy
import re
import base64
import urllib
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from bs4 import BeautifulSoup

from stack.items import StackItem, UserItem


class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['vietsingle.com']
    start_urls = [
        "http://vietsingle.com/search.php?page=1&show=0&next=&search=both&state=&country=&start=18&stop=80&month=&city=&k=5&l=1&pix="
        #"http://vietsingle.com/search.php?page=1&show=0&next=&search=female&state=&country=VN&start=18&stop=35&month=&city=&k=5&l=1&pix="
    ]

    rules = (
        Rule(LinkExtractor(allow=r'search.php\?page=\d+&'), callback='parse_item', follow=True),
        #rule for extract personal pages
        #Rule(LinkExtractor(allow=r'pro.php\?ID=\d+'), callback='parse_item_user', follow=True),
    )

    user_mapping = dict(
        name = "Name:",ip_date = "IP & Posted by:",modified_date = "Updated by:",gender = "Gender:",
        age = "Age:", height = "Height:", weight="Weight:", body="Body Type:",
        city ="From City:", country = "Country:", religion ="Religion:", education ="Education:",
        job = "Occupation:", smoking="Smoker:", drinking="Drinker:", status="Marital Status:",
        goal="My goal:", free_time="Free Time:", i_am="I Am:", looking_for="Looking For:"
    )
    

    def parse_item_user(self, response):
        
        user = UserItem()
        # go to the user by link
        # parse the link to create a new item
        # save in database
        soup = BeautifulSoup(response.body)

        # search for all keys and creae
        
        table = soup.find("table", attrs={"bgcolor":"#D0BFDE"})        
        tr = table.find_all('tr')#[1:-2]
        user['user_id'] = table.find_all('tr')[-1].get_text()[table.find_all('tr')[-1].get_text().find('(')+5:table.find_all('tr')[-1].get_text().find(')')]
        for tr in table.find_all('tr')[1:-2]:
            _att = tr.find_all('td')[0].get_text().strip()# the field, the bold one
            '''now is the list of if'''
            if 'Name:' in _att:
                user['name'] = tr.find_all('td')[1].get_text().strip()
            elif 'IP & Posted by:' in _att:
                user['ip_date'] = tr.find_all('td')[1].get_text().strip()# value
            elif 'Updated by:' in _att:
                user['modified_date'] = tr.find_all('td')[1].get_text().strip()# value
            elif 'Gender:' in _att:
                user['gender'] = tr.find_all('td')[1].get_text().strip()# value
            elif 'Age:' in _att:
                user['age'] = tr.find_all('td')[1].get_text().strip()# value
            elif 'Height:' in _att :
                user['height'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Weight:" in _att:            
                user['weight'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Body Type:" in _att:    
                user['body'] = tr.find_all('td')[1].get_text().strip()# value
            elif "From City:" in _att:
                user['city'] = tr.find_all('td')[1].get_text().strip()# value       
            elif "State/Province:" in _att:
                user['state'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Zip:" in _att:    
                user['zip_code'] = tr.find_all('td')[1].get_text().strip()# value    
            elif "Country:" in _att:
                user['country'] = tr.find_all('td')[1].get_text().strip()# value       
            elif "Religion:" in _att:    
                user['religion'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Education:" in _att:
                user['education'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Occupation:" in _att:    
                user['job'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Smoker:" in _att:                
                user['smoking'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Drinker:" in _att:                
                user['drinking'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Marital Status:" in _att:
                user['status'] = tr.find_all('td')[1].get_text().strip()# value
            elif "My goal:" in _att:    
                user['goal'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Free Time:" in _att:
                user['free_time'] = tr.find_all('td')[1].get_text().strip()# value
            elif "I Am:" in _att:
                user['i_am'] = tr.find_all('td')[1].get_text().strip()# value
            elif "Looking For:" in _att:
                user['looking_for'] = tr.find_all('td')[1].get_text().strip()# value
                
        #now extracting all the images
        image_tags = soup.find_all('img')[1:-1] #not the first and the last one
        image_links = []
        user_images = {}
        for img in image_tags:
            if '.gif' in img['src']:#???
                log.msg(message="This is GIF. Dont store")
            if '/img2/' in img['src']:
                imgurl = img['src'].replace('/img2/','/img/')
                img_name = imgurl.split('/')[-1].replace('.','__')                
                image_links.append(img['src'])  
                img = urllib.urlopen(imgurl)
                img_data = img.read()
                b64 = base64.b64encode(img_data)
                #dont store image any more, but store the link to images
                #user_images[img_name] = b64
                user_images[img_name] = img['src']
        user['user_images'] = user_images
        yield user        
        
        
    def parse_item(self, response):
        
        soup = BeautifulSoup(response.body)
        #get the content table
        table = soup.find("table", attrs={"bgcolor":"#D0BFDE"})
        #get the heading
        headings = [th.get_text() for th in table.find("tr",attrs={"bgcolor":"#ffffff"}).find_all("td")]
        
        datasets = []
        for row in table.find_all("tr")[1:]:
            #dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            #datasets.append(dataset)
            item = StackItem()
            tds = row.find_all("td") #get data            
            item['name'] = tds[0].get_text().strip()
            item['gender'] = tds[1].get_text().strip()
            item['image'] = tds[2].get_text().strip()
            item['picture'] = tds[3].get_text().strip()
            item['location'] = tds[4].get_text().strip()
            item['views'] = tds[5].get_text().strip()
            item['log_date'] = tds[6].get_text().strip()
            item['user_id'] = re.search("ID=(\d+)&",str(tds[0])).group(1).strip()
            item['user_url'] = row.find_all('td')[0].find_all('a')[0]['href'].strip()
            yield item
            


            
