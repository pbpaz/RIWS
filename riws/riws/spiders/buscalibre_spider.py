import scrapy
from riws.items import PazBookItem 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ByscalibreSpider(CrawlSpider):
    name="buscalibre_spider"
    
    allowed_domains = ['www.buscalibre.es']

    file = open('categories.txt', 'a', encoding='utf-8')
    cats = []
    #Start URL
    start_urls = [
        'https://www.buscalibre.es'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            "riws.pipelines.ProcessBuscalibreSpiderPipeline": 1,
            "riws.pipelines.JsonWriterPipeline": 2,
        }
    }

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
        item['author'] = response.css('p.font-weight-light a.font-color-bl::text').get()
        item['editorial'] = response.css('div#metadata-editorial a::text').get()
        item['edition_date'] = response.css('div#metadata-ano::text').get()
        item['category'] =  response.css('div[id="metadata-categorías"] a::text').getall()

        for cat in item['category']:
            if cat.strip() not in self.cats:
                self.cats.append(cat.strip())
                self.file.write(str(cat.strip()))
                self.file.write('\n')
        
        item['isbn'] = response.css('div#metadata-isbn13::text').get()
        item['pages'] = response.css('div[id="metadata-número páginas"]::text').get()
        item['synopsis'] = response.css('span#texto-descripcion *::text').getall()
        item['cover'] = response.css('img#imgPortada::attr(data-src)').get()
        item['cost'] = response.css('p.precioAhora span::text').get()
        yield item
