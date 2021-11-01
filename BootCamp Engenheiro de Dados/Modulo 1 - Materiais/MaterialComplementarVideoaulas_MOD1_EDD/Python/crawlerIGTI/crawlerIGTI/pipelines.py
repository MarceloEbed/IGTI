# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter

import json
import codecs

class CrawlerigtiPipeline:
    
    def open_spider(self, spider):
        #Abre arquivo para armazenar os itens raspados
        if spider.name == 'crawlingIGTIBlog':
            #print('Spider: crawlingIGTIBlog')
            self.file = codecs.open('crawled_pages.json', 'w', encoding='utf8')
        elif spider.name == 'scrapingIGTIBlog':
            #print('Spider: scrapingIGTIBlog')
            self.file = codecs.open('scraped_items.json', 'w', encoding='utf8')
        #print('Open json file.')

        self.file.write("[")

    def close_spider(self, spider):
        #Abre arquivo
        self.file.write("]")        
        self.file.close()
        #print('Close json file.')

    def write_file(self, item, spider):
        # Os itens raspados serão gravados no arquivo 'scraped_items.json'.
        line = json.dumps(
            dict(item), indent = 4,
            sort_keys = True,
            separators = (',', ': ')
        , ensure_ascii=False) + ",\n"
        self.file.write(line)
        
       
    def process_item(self, item, spider):
        
        if spider.name == 'scrapingIGTIBlog':
            if item['comentarios_artigo'] == 'Comentar':
                item['comentarios_artigo'] = '0 comentários'

        
        CrawlerigtiPipeline.write_file(self, item, spider)
        
        return item
