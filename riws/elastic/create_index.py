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
            "author": {"type": "text", 
                       "fields": {
                           "raw": {
                               "type": "keyword"
                           }
                       }},
            "editorial": {"type": "text",
                          "fields": {
                           "raw": {
                               "type": "keyword"
                           }
                       }},
            "edition_date": {"type": "integer"},
            "category": {"type": "text", 
                         "fields": {
                           "raw": {
                               "type": "keyword"
                           }
                       }},
            "isbn": {"type": "keyword"},
            "pages": {"type": "integer"},
            "synopsis": {"type": "text"},
            "cover": {"type": "text"},
            "cost": {"type": "float"}
        }
    }
}

es.indices.create(index=index_name, body=mapping)
print(f"Index '{index_name}' succesfully created.")