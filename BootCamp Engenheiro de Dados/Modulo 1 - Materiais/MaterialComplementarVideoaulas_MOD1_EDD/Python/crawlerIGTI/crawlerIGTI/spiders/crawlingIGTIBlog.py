import scrapy

from crawlerIGTI.items import CrawlerIGTIItem

class CrawlingigtiblogSpider(scrapy.Spider):
    
    name = 'crawlingIGTIBlog'
    
    #allowed_domains = ['www.igti.com.br/blog']
    
    start_urls = ['http://www.igti.com.br/blog/']


    def parse(self, response):        
        self.log('Acessando a URL: %s' % response.url)
        
        categories = response.xpath("//nav[@class='gridlove-main-navigation']//li//a")
        
        item = CrawlerIGTIItem()
        
        for category in categories:
            url = category.xpath('@href').extract_first()
            self.log('Categoria %s' % category.xpath('text()').extract_first())            

            yield response.follow(url, self.parse_category)
            
        item['titulo_pagina']  = response.css("title ::text").extract_first()
        item['url_pagina'] = response.url
        item['categoria'] = 'HOME'
        
        yield item
        
    def parse_category(self, response):
        self.log('Acessando a URL: %s' % response.url)
        
        item = CrawlerIGTIItem()
        
        #articles = response.xpath("//article")
        item['titulo_pagina']  = response.css("title ::text").extract_first()
        item['url_pagina'] = response.url
        item['categoria'] = response.xpath("//h1[@class='h2']/text()").extract_first()
        
        yield item        