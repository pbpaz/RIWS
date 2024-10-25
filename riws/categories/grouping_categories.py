import json
from fuzzywuzzy import fuzz
import copy

# Definir categorías generales
keywords = {
    "Poesía": ["poesía", "lírica"],
    "Hobbies": ["hobbie", "tiempo libre"],
    "Salud": ["salud", "saude", "medicina"],
    "Educación": ["educacion", "ensino", "enseñanza"],
    "Thriller": ["thriller"],
    "Cómic": ["banda deseñada", "cómic", "banda diseñada"],
    "Romance": ["romance", "romántica", "amor"],
    "Ficción": ["Ficción", "Ciencia Ficción"],
    "Fantasía": ["Fantasía"],
    "Misterio": ["Misterio"],
    "Historia": ["Historia", "histórica", "siglo", "guerra"],
    "Biografía": ["biografía"],
    "Ensayo": ["ensayo"],
    "Psicología": ["psicología"],
    "Filosofía": ["filosfía"],
    "Ingeniería": ["ingenieria"],
    "Autoayuda": ["autoayuda"],
    "Religión": ["religión", "iglesia", "cristianismo", "judaismo", "budaismo"],
    "Biología": ["biologia"],
    "Ciencia y Tecnología": ["Ciencia y Tecnología", "ciencias", "tecnología"],
    "Arte": ["arte", "escultura", "pintura", "musica", "cine", "pelicula", "barroco", "gotico", "rococo", "renacimiento"],
    "Cocina": ["cocina", "recetas"],
    "Literatura Infantil": ["infantil"],
    "Literatura Juvenil": ["juvenil"],
    "Manga": ["manga", "shonen"], 
    "Novela": ["novela"], 
    "Mapas": ["mapas", "atlas"], 
    "Deporte": ["deporte", "futbol", "tenis", "baloncesto", "atletismo"], 
    "Países": ["afganistán", "albania", "alemania", "andorra", "angola", "antigua y barbuda", "arabia saudita",
    "argelia", "argentina", "armenia", "australia", "austria", "azerbaiyán", "bahamas", "bahrein",
    "bangladés", "barbados", "baréin", "bélgica", "bielorrusia", "birmania", "bolivia", "bosnia y herzegovina",
    "botsuana", "brasil", "brunéi", "bulgaria", "burkina faso", "burundi", "cabo verde", "camerún",
    "canadá", "chad", "checoslovaquia", "chile", "china", "chipre", "colombia", "comoras", "costa de marfil",
    "costa rica", "croacia", "cuba", "dinamarca", "dominica", "ecuador", "egipto", "el salvador", "emiratos árabes unidos",
    "eslovenia", "españa", "estados unidos", "estonia", "eswatini", "ethiopía", "filipinas", "finlandia",
    "francia", "gabón", "gambia", "georgia", "ghana", "gibraltar", "granada", "grecia", "guatemala",
    "guinea", "guinea-bisáu", "guinea ecuatorial", "haití", "holanda", "hungría", "india", "indonesia",
    "irán", "iraq", "irlanda", "islandia", "israel", "italia", "jamaica", "japón", "jordania", "kazajistán",
    "kenia", "kirguistán", "kiribati", "korea del norte", "korea del sur", "kuwait", "laos", "lesoto",
    "letonia", "líbano", "libia", "lituania", "luxemburgo", "madagascar", "malasia", "malawi", "maldivas",
    "mali", "malta", "marruecos", "mauricio", "mauritania", "mexico", "micronesia", "mónaco", "mongolia",
    "montenegro", "mozambique", "namibia", "nauru", "nepal", "nicaragua", "niger", "nigeria", "noruega",
    "nueva zelanda", "omán", "países bajos", "pakistán", "panamá", "papúa nueva guinea", "paraguay", "perú",
    "polonia", "portugal", "reino unido", "reino unido", "república checa", "república del congo", "república dominicana",
    "república centroafricana", "república del surinam", "ruanda", "rumanía", "rusia", "samoa", "san cristóbal y nieves",
    "san marino", "san vicente y las granadinas", "santa lucía", "santo tomé y príncipe", "serbia", "singapur", "siria",
    "somalia", "sudáfrica", "sudán", "sudán del sur", "suecia", "suiza", "tailandia", "tanzania", "taiwán", "togo",
    "tonga", "trinidad y tobago", "túnez", "turkmenistán", "turquía", "tuvalu", "ucrania", "uganda", "uruguay",
    "venezuela", "vietnam", "yemen", "zambia", "zimbabue"]
}

# Keyword grouping function
def group_by_keywords(categories, dic):
    
    for category in categories:
        for general, key_list in dic.items():
            if any(keyword in category.lower() for keyword in key_list):
                if category not in dic[general]:
                    dic[general].append(category)

    return dic

# Levenshtein similarity grouping
def group_by_similarity(categories, dic):
    
    for category in categories:
        for general, key_list in keywords.items():
            for key in key_list:
                similarity = fuzz.ratio(category.lower(), key.lower())

                if similarity >= threshold:
                    if category not in dic[general]:
                        dic[general].append(category)
                    break

    return dic

#Combine dict function
def combine_dictionaries(dict1, dict2):
    combined_dict = copy.deepcopy(dict1)
    for key, values in dict2.items():
        for value in values:
            if value not in combined_dict[key]:
                combined_dict[key].append(value)
    return combined_dict


#Loading the initial data
with open("buscalibre_unique_categories.txt", "r", encoding="utf-8") as file:
    buscalibre_content = [linea.strip() for linea in file.readlines()]
with open("paz_unique_categories.txt", "r", encoding="utf-8") as file:
    paz_content = [linea.strip() for linea in file.readlines()]
with open("planeta_categories.txt", "r", encoding="utf-8") as file:
    planeta_content = [linea.strip() for linea in file.readlines()]


#Grouping by keywords
initial_dic = copy.deepcopy(keywords)

res1 = group_by_keywords(buscalibre_content, initial_dic)
res2 = group_by_keywords(planeta_content, res1)
keys_dict = group_by_keywords(paz_content, res2)


#Similarity grouping
threshold = 75
initial_dic_2 = copy.deepcopy(keywords)

similarity_1 = group_by_similarity(buscalibre_content, initial_dic_2)
similarity_2 = group_by_similarity(planeta_content, similarity_1)
similarity_dict = group_by_similarity(paz_content, similarity_2)

#Combining dicts
final_dict = combine_dictionaries(keys_dict, similarity_dict)

print(sum(len(v) for v in final_dict.values()), "\n")

#Saving the final dict
with open("categories_dict.json", 'w', encoding='utf-8') as file:
    # Guarda el diccionario en formato JSON
    json.dump(final_dict, file, ensure_ascii=False, indent=4)