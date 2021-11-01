import scrapy

from crawlerIGTI.items import ScraperIGTIItem

class ScrapingigtiblogSpider(scrapy.Spider):
    
    name = 'scrapingIGTIBlog'
    
    #allowed_domains = ['www.igti.com.br/blog']
    #start_urls = ['http://www.igti.com.br/blog/']

    def __init__(self):
        self.start_urls = ['https://www.igti.com.br/blog/']  

    def parse(self, response):
        
        self.log('Acessando a URL: %s' % response.url)
        
        item = ScraperIGTIItem() 
        
        item['titulo_pagina']  = response.css("title ::text").extract_first()
        item['url_pagina'] = response.url
        
        articles = response.xpath("//article")
        count_article = 0
        
        for article in articles:

            count_article += 1
            self.log('Artigo %s' % str(count_article))
            
            categories = article.xpath(".//div/div[@class='entry-category']//a")
            #print('Categorias %s' % str(len(categories)))
            
            if len(categories) == 1:
                
                item['categoria_artigo'] = ''.join(categories.xpath('text()').get())
                item['categoria_URL'] = ''.join(categories.xpath('@href').get())

                 
            elif len(categories) > 1:

                item['categoria_artigo'] = []
                item['categoria_URL'] = []
                i = 0
                
                while i < len(categories):
                    
                    item['categoria_artigo'].append(''.join(categories.xpath('text()')[i].get()))
                    item['categoria_URL'].append(''.join(categories.xpath('@href')[i].get()))
                    i += 1                   
                  
            title = article.xpath(".//h2[@class='entry-title h3']//a")
            
            item['titulo_artigo'] = ''.join(title.xpath('text()').get())
            item['url_artigo'] = ''.join(title.xpath('@href').get())

            metadata = article.xpath(".//div/div[@class='entry-meta']")
            data = metadata.xpath(".//div[@class='meta-item meta-date']/span[@class='updated']")		
            item['dtPostagem_artigo'] = ''.join(data.xpath('text()').get())            
            #print('Data da postagem: ', item['dtPostagem'])
            
            comentario = metadata.xpath(".//div[@class='meta-item meta-comments']//a//span[@class='dsq-postid']")            
            item['comentarios_artigo'] = ''.join(comentario.xpath('text()').get())
            #print('Quantidade de comentários: ', item['comentarios'])
             
            visao = metadata.xpath(".//div[@class='meta-item meta-views']")
            item['visualizacoes_artigo'] = ''.join(visao.xpath('text()').get())
            #print('Quantidade de visualizações: ', item['visualizacoes'])
            
            #print('Type(item[categoria_URL]) - ' % type(item['categoria_URL']))
            yield item
                    