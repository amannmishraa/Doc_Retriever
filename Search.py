from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Index document into Elasticsearch (store document embeddings here)
def index_document(doc_id, text, embedding):
    es.index(index="documents", id=doc_id, body={"text": text, "embedding": embedding})
