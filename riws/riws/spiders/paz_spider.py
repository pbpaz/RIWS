import scrapy
from riws.items import PazBookItem 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class PazSpider(CrawlSpider):
    name="paz_spider"
    
    allowed_domains = ['www.librariapaz.gal']

    #Start URL
    start_urls = [

        'https://www.librariapaz.gal/es/index.php'
    ]


    #Rules for the spider
    rules = (

        #Rule for the concrete book
        Rule(LinkExtractor(allow=(r'/es/libro/')), callback='parse', follow = False),
        
        #Rule for the navigation on the sections
        Rule(LinkExtractor(allow=(r'/es/libros-de/.+pagSel=\d+')), follow=True),

        #Rule for the sections
        Rule(LinkExtractor(allow=(r'/es/libros-de/ficcion-020B/')), follow = True),
    )


    #Parse method to extract the information of the concrete book
    def parse(self, response):

        for book in response.css('div.fichaDetalle.col-sm-9'):
            item = PazBookItem()
            item['name'] = book.css('h1#titulo::text').get()
            item['author'] = book.css('span.nomesigas::text').get()
            item['editorial'] = book.css('dd.editorial span.nomesigas::text').get()
            item['edition_date'] = book.css('dt:contains("Año de edición") + dd::text').get()
            item['category'] = book.css('dd a::text').get()
            item['isbn'] = book.css('dt:contains("ISBN") + dd::text').get()
            item['pages'] = book.css('dt:contains("Páginas") + dd::text').get()
            item['synopsis'] = ' '.join(book.xpath('//*[@id="tabsinopsis"]/p[@class="bodytext"]//text()').getall()).strip()

            yield item
