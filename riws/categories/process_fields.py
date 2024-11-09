import json

with open("../books_paz_parsed.json", 'r', encoding='utf-8') as file:
    # Carga el contenido del archivo JSON en un diccionario
    books = json.load(file)

for element in books:
    if "name" in element:
        element["name"] = ' '.join(element["name"].split()).title()
    if "author" in element:
        element["author"] = ' '.join(element["author"].split()).title()
    if "editorial" in element:
        element["editorial"] = ' '.join(element["editorial"].split()).title()
    
with open("../books_paz_final.json", "w",encoding='utf-8') as file:
    json.dump(books, file, indent=4, ensure_ascii=False)
