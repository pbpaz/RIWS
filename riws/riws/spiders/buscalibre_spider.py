import scrapy
from riws.items import PazBookItem 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ByscalibreSpider(CrawlSpider):
    name="buscalibre_spider"
    
    allowed_domains = ['www.buscalibre.es']

    #Start URL
    start_urls = [

        'https://www.buscalibre.es'
    ]

    #Rules for the spider
    rules = (

        #Rule for the concrete book
        Rule(LinkExtractor(allow=(r'/libro-')), callback='parse', follow = False),
        #Rule for the sections
        Rule(LinkExtractor(allow=(r'/libros/')), follow = True),
    )

    #Parse method to extract the information of the concrete book
    def parse(self, response):

        item = PazBookItem()
        item['url'] = response.url
        item['name'] = response.css('p.tituloProducto::text').get()
        item['author'] = response.css('p.font-weight-light a.font-color-bl::text').get().strip()
        item['editorial'] = response.css('div#metadata-editorial a::text').get().strip()
        item['edition_date'] = response.css('div#metadata-ano::text').get().strip()
        categories =  response.css('div[id="metadata-categorías"] a::text').getall()
        cat2 = []
        for cat in categories:
            cat2.append(cat.strip())
        item['category'] = cat2
        item['isbn'] = response.css('div#metadata-isbn13::text').get().strip()
        item['pages'] = response.css('div[id="metadata-número páginas"]::text').get().strip()
        item['synopsis'] = "\n".join(response.css('span#texto-descripcion *::text').getall())
        item['cover'] = response.css('img#imgPortada::attr(data-src)').get()
        item['cost'] = response.css('p.precioAhora span::text').get()
        yield item
