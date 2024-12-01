from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch(hosts=["http://localhost:9200"])

index_name = "books"

with open ('../data/books_buscalibre_parsed.json', "r", encoding="utf-8") as file:
    buscalibre = json.load(file)
with open ('../data/books_paz_parsed.json', "r", encoding="utf-8") as file:
    paz = json.load(file)
with open ('../data/books_planeta_parsed.json', "r", encoding="utf-8") as file:
    planeta = json.load(file)

books = buscalibre + paz + planeta

actions = [
    {
        "op_type": "index",
        "_index": index_name,
        "_id": i,
        "_source":book
    }
    for i, book in enumerate(books)
]

try:
    helpers.bulk(es, actions, chunk_size=1000)
    print("All books inserted.")
except Exception as e:
    print("Error during insertion:", e)