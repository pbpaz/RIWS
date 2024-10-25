from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=["http://localhost:9200"]
)

index_name = "books"

mapping = {
    "mappings": {
        "properties": {
            "url": {"type": "text"},
            "name": {"type": "text"},
            "author": {"type": "text"},
            "author_keyword": {"type": "keyword"},
            "editorial": {"type": "text"},
            "editorial_keyword": {"type": "keyword"},
            "edition_date": {"type": "integer"},
            "category": {"type": "text"},
            "category_keyword": {"type": "keyword"},
            "isbn": {"type": "keyword"},
            "isbn_keyword": {"type": "keyword"},
            "pages": {"type": "integer"},
            "synopsis": {"type": "text"},
            "cover": {"type": "text"},
            "cost": {"type": "float"}
        }
    }
}

es.indices.create(index=index_name, body=mapping)
print(f"Índice '{index_name}' creado con éxito.")