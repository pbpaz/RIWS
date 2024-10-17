import scrapy
import json
import jsonschema
from riws.items import PazBookItem 
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class PlanetadelibrosSpider(CrawlSpider):
    name = 'planetadelibros'
    allowed_domains = ['planetadelibros.com']
    start_urls = ['https://www.planetadelibros.com/']

    rules = (
        #categorias
        Rule(
            LinkExtractor(allow=r'/libros/[a-zA-Z\-]+/\d+$'),
            follow=True
        ),
        Rule(
            LinkExtractor(allow=r'/libros/[a-zA-Z\-]+/\d+/p/\d+$'), 
            follow=True
        ),

        Rule(
            LinkExtractor(allow=r'https://www.planetadelibros.com/[a-zA-Z\-]+/\d+$'), 
            callback='parse_book',
            follow=False
        ),
    )

    def parse_book(self, response):
        book_title = response.css('h1.FichaLibro_fichaLibro__titulo__zoYiu::text').get()
        author = response.css('ul.LibroAutores_autoresList__ND_Mc li.LibroAutores_autoresListItem__i2Pkw a::text').get()
        category = response.css('td.FichaTecnica_fichaTecnicaValue__Tnr08 ul.FichaTecnica_fichaTecnicaList__Pe77f li a::text').getall()
        editorial = response.css('table.FichaTecnica_fichaTecnicaTabla__VKBCJ tr:contains("Editorial") td.FichaTecnica_fichaTecnicaValue__Tnr08 a::text').get()
        isbn = response.css('table.FichaTecnica_fichaTecnicaTabla__VKBCJ tr:contains("ISBN") td.FichaTecnica_fichaTecnicaValue__Tnr08::text').get()
        pages = response.css('table.FichaTecnica_fichaTecnicaTabla__VKBCJ tr:contains("Páginas") td.FichaTecnica_fichaTecnicaValue__Tnr08::text').get()
        
        json_data = response.css('script#\\__NEXT_DATA__::text').get()
        
        cover = None
        if json_data:
            data = json.loads(json_data)
            cover = data.get('props', {}).get('pageProps', {}).get('page', {}).get('schema', {}).get('image', None)

            if isinstance(cover, dict) and 'path' in cover:
                cover = cover['path']

        synopsis = ' '.join(response.css('div.mantine-Text-root p::text').getall())
        cost = response.css('button.OpcionesCompra_btnFormato__LQpT9 span.OpcionesCompra_btnFormato__precio__k3qxO::text').get()

        item = PazBookItem(
            name=book_title,
            author=author,
            editorial=editorial,
            isbn=isbn,
            cover=cover,
            pages=pages,
            cost=cost,
            synopsis=synopsis,
            category=category
        )

        yield item   

