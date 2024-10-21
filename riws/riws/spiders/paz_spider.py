import scrapy
from riws.items import PazBookItem 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class PazSpider(CrawlSpider):
    name="paz_spider"
    
    allowed_domains = ['www.librariapaz.gal']

    #Start URL
    start_urls = [
        'https://www.librariapaz.gal/es/libro/manga-art_720130'
        # 'https://www.librariapaz.gal/es/index.php'
    ]


    #Rules for the spider
    rules = (

        #Rule for digital books without information
        Rule(LinkExtractor(allow=(r'/es/libros-de/libro-dixital')), follow = False),

        #Rule for the concrete book
        Rule(LinkExtractor(allow=(r'/es/libro/')), callback='parse', follow = False),
        
        #Rule for the navigation on the sections
        Rule(LinkExtractor(allow=(r'/es/libros-de/.+pagSel=\d+')), follow=True),

        #Rule for the sections
        Rule(LinkExtractor(allow=(r'/es/libros-de/')), follow = True),
    )


    #Parse method to extract the information of the concrete book
    def parse(self, response):

        item = PazBookItem()
        item['url'] = response.url
        item['name'] = response.css('h1#titulo::text').get()
        item['author'] = response.css('span.nomesigas::text').get()
        item['editorial'] = response.css('dd.editorial span.nomesigas::text').get()
        item['edition_date'] = response.css('dt:contains("Año de edición") + dd::text').get()
        item['category'] = response.css('dd a::text').get()
        item['isbn'] = response.css('dt:contains("ISBN") + dd::text').get()
        item['pages'] = response.css('dt:contains("Páginas") + dd::text').get()
        item['synopsis'] = response.css('div#tabsinopsis p.bodytext::text').getall()
        item['cover'] = response.css('div#detimg img#detportada::attr(src)').get()
        item['cost'] = response.css('div.infoprices span.despues::text').get()
        yield item
