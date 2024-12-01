import json

with open("../data/books_data_paz.json", "r", encoding="utf-8") as file:
    paz_data = json.load(file)

with open("categories_dict.json", 'r', encoding='utf-8') as file:
    # Carga el contenido del archivo JSON en un diccionario
    categories_dict = json.load(file)


for element in paz_data:
    if "category" in element and isinstance(element["category"], list):

        if not element["category"]: 
            element["category"] = ["Otros"]

        unique_categories = set()

        for i, single_category in enumerate(element["category"]):
            hit = False
            for key, value in categories_dict.items():
                if single_category in value:
                    unique_categories.add(key)
                    hit = True
            if not hit:
                unique_categories.add("Otros")

    element["category"] = list(unique_categories)

with open("../data/books_pazaaaaa_parsed.json", "w",encoding='utf-8') as file:
    json.dump(paz_data, file, indent=4, ensure_ascii=False)