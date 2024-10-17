# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import json

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

