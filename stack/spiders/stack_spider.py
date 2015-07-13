from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem 
########################################################################
class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["vietsingle.com"]
    start_urls = [
        "http://vietsingle.com/search.php?page=1&show=0&next=&search=both&state=&country=&start=18&stop=80&month=&city=&k=5&l=1&pix=",
    ]
    
    #----------------------------------------------------------------------
    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')
        
        for question in questions:
            item = StackItem()        
            item['title'] = question.xpath('a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath('a[@class="question-hyperlink"]/@href').extract()[0]
            yield item 
            
        
        
    
    