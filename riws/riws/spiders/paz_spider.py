import scrapy
from riws.items import PazBookItem 

class PazSpider(scrapy.Spider):
    name="paz_spider"

    #Start URL
    start_urls = [

        'https://www.librariapaz.gal/es/libro/asesinato-en-el-orient-express_520089'
    ]

    #Parse method to extract the information
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

        #Follow the next page link if available

