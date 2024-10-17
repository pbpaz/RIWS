import scrapy
from riws.items import BookItem 
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class PlanetadelibrosSpider(CrawlSpider):
    name = 'planetadelibros'
    allowed_domains = ['planetadelibros.com']
    #start_urls = ['https://www.planetadelibros.com/']
    start_urls = ['https://www.planetadelibros.com/libro-el-mejor-libro-del-mundo/399554']

    rules = (
        #Rule(
        #    LinkExtractor(allow=r'/libros/[a-zA-Z\-]+/\d+$'), 
        #    callback='parse_item',
        #    follow=True
        #),
        #Rule(
        #    LinkExtractor(allow=r'/libros/[a-zA-Z\-]+/\d+/p/\d+$'), 
        #    follow=True
        #),
        #Rule(
        #    LinkExtractor(allow=r'/[a-zA-Z\-]+/\d+$'), 
        #    callback='parse_book',
        #    follow=False
        #),
        Rule(
            LinkExtractor(allow='https://www.planetadelibros.com/libro-el-mejor-libro-del-mundo/399554'), 
            callback='parse_book',
            follow=False
        ),
    )

    def parse_item(self, response):
        with open('categorias.txt', 'a', encoding='utf-8') as f:
            f.write(f"{response.url}\n")
        
        print(f"Procesando URL: {response.url}")
        
    def parse_book(self, response):
        book_title = response.css('h1.FichaLibro_fichaLibro__titulo__zoYiu::text').get()

        author = response.css('ul.LibroAutores_autoresList__ND_Mc li.LibroAutores_autoresListItem__i2Pkw a::text').get()

        editorial = response.css('table.FichaTecnica_fichaTecnicaTabla__VKBCJ tr:contains("Editorial") td.FichaTecnica_fichaTecnicaValue__Tnr08 a::text').get()

        isbn = response.css('table.FichaTecnica_fichaTecnicaTabla__VKBCJ tr:contains("ISBN") td.FichaTecnica_fichaTecnicaValue__Tnr08::text').get()

        pages = response.css('table.FichaTecnica_fichaTecnicaTabla__VKBCJ tr:contains("Páginas") td.FichaTecnica_fichaTecnicaValue__Tnr08::text').get()

        cover = response.css('div#libroGallery img::attr(src)').get()

        synopsis = ' '.join(response.css('div.mantine-Text-root p::text').getall())

        cost = response.css('button.OpcionesCompra_btnFormato__LQpT9 span.OpcionesCompra_btnFormato__precio__k3qxO::text').get()

        item = BookItem(
            name=book_title,
            author=author,
            editorial=editorial,
            isbn=isbn,
            cover=cover,
            pages=pages,
            cost=cost,
            synopsis=synopsis
        )

        with open('books_data.txt', 'a', encoding='utf-8') as f:
            f.write(f"{item}\n")

        yield item    

