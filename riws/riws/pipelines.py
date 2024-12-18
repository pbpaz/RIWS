# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import re

class ProcessPlanetadelibrosSpider:

    def process_item(self, item, spider):

        #Cost
        if item['cost'] is not None:
            t1 = item.get('cost')
            t2 = t1.split()
            item['cost'] = float(t2[0].replace(',', '.'))

        #Pages
        if item['pages'] is not None:
            item['pages'] = int(item.get('pages'))

        #ISBN
        if item['isbn'] is not None:
            item['isbn'] = int(item.get('isbn').replace('-', ''))

        #Category
        if item['category'] is not None:
            if isinstance(item['category'], list):
                if len(item['category']) > 0:
                    item['category'].pop(0)
                if len(item['category']) > 0:
                    item['category'].pop(0)    
                if len(item['category']) > 0:
                    item['category'].pop()
         
        #Synopsis
        if item['synopsis'] is not None:
            item['synopsis'] = item.get('synopsis').replace('\n', '').replace('\r', '').replace('\t', '')

        self.file = open('categories.txt', 'a', encoding='utf-8')
        for element in item['category']:
            self.file.write(f"{element}\n")     
        
        return item

class ProcessPazSpiderPipeline:

    def process_item(self, item, spider):

        if spider.name != 'paz_spider':
            return item
        
        #Author
        if item['author'] is not None:
            t1 = item.get('author')
            t2 = t1.split(",")
            if len(t2) > 1:
                item['author'] = t2[1] + " " + t2[0]

        #Edition_date
        if item['edition_date'] is not None:
            item['edition_date'] = int(item.get('edition_date'))

        #Cost
        if item['cost'] is not None:
            t1 = item.get('cost')
            t2 = t1.split()
            item['cost'] = float(t2[0].replace(',', '.'))

        #Pages
        if item['pages'] is not None:
            item['pages'] = int(item.get('pages'))

        #ISBN
        if item['isbn'] is not None:
            item['isbn'] = int(item.get('isbn').replace('-', ''))
         
        #Synopsis
        if item['synopsis'] is not None:
            item['synopsis'] = " ".join(item.get('synopsis'))
            item['synopsis'] = item.get('synopsis').replace('\n', '').replace('\r', '').replace('\t', '')

        #Category
        t1 = item.get('category')
        if t1 == 'Sin clasificar':
            item['category'] = []
        else:
            t1 = item.get('category')
            t2 = re.split(r' e |\. | - ', t1)
            if len(t2) > 1:
                item['category'] = t2
            else:
                item['category'] = [item.get('category')]
            
        self.file = open('categories.txt', 'a', encoding='utf-8')
        for element in item['category']:
            self.file.write(f"{element}\n")
        
        return item
        

class ProcessBuscalibreSpiderPipeline:

    def process_item(self, item, spider):

        if spider.name != "buscalibre_spider":
            return item
        
        #Author
        if item['author'] is not None:
            authors = item['author'].strip().split(';')
            final_auth= []
            for author in authors:
                final_name=author
                if "," in author:
                    words = author.split(",")
                    final_name = words[1] + " " + words[0]
                final_auth.append(final_name.strip())
            item['author'] = final_auth

        if item['name'] is not None:
            item['name'] = item['name'].strip()
        #Editorial
        if item['editorial'] is not None:
            item['editorial'] = item['editorial'].strip()
        #Edition_date
        if item['edition_date'] is not None:
            item['edition_date'] = int(item['edition_date'].strip())

        #Cost
        if item['cost'] is not None:
            t1 = item['cost']
            t2 = t1.split()
            item['cost'] = float(t2[0].replace(',', '.'))

        #Pages
        if item['pages'] is not None:
            item['pages'] = int(item['pages'].strip())

        #ISBN
        if item['isbn'] is not None:
            item['isbn'] = int(item['isbn'].strip())
         
        #Synopsis
        if item['synopsis'] is not None:
            item['synopsis'] = " ".join(item['synopsis'])
            item['synopsis'] = item.get('synopsis').replace('\n', '').replace('\r', '').replace('\t', '')

        #Category
        categories = item.get('category')
        cat2 = []
        for cat in categories:
            cat2.append(cat.strip())
        item['category'] = cat2
        
        return item

class JsonWriterPipeline:
    def open_spider(self, spider):
        # Abrir un archivo para escribir en modo de escritura cuando el spider se inicie
        self.file = open('books_data.json', 'w', encoding='utf-8')
        self.file.write('[')
        self.first_item = True

    def close_spider(self, spider):
        # Cerrar el archivo cuando el spider se cierre
        self.file.write(']\n')  # Escribir el final del array JSON
        self.file.close()
 
    def process_item(self, item, spider):

        for field, value in item.items():
            if isinstance(value, str):
                item[field] = value.encode('utf-8').decode('utf-8', 'ignore')

        # JSON conversion
        if not self.first_item:
            self.file.write(',\n')
        self.first_item = False
        line = json.dumps(dict(item), indent=4, ensure_ascii=False)
        self.file.write(line)
        return item
