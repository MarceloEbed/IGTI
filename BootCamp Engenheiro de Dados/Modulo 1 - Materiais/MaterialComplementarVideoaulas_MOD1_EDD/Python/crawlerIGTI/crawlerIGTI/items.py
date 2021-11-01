# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScraperIGTIItem(scrapy.Item):
    
    #Para cada página de categoria:
    url_pagina = scrapy.Field()
    titulo_pagina = scrapy.Field()

    #Para cada artigo da página:
    categoria_artigo = scrapy.Field()
    categoria_URL = scrapy.Field()
    titulo_artigo = scrapy.Field()
    url_artigo = scrapy.Field()
    dtPostagem_artigo = scrapy.Field()
    comentarios_artigo = scrapy.Field()
    visualizacoes_artigo = scrapy.Field()

class CrawlerIGTIItem(scrapy.Item):
    
    #Para cada página de categoria:
    titulo_pagina = scrapy.Field()
    categoria = scrapy.Field()
    url_pagina = scrapy.Field()