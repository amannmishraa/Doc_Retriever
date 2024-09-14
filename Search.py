# search.py

from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Index document into Elasticsearch
def index_document(doc_id, text, embedding):
    es.index(index="documents", id=doc_id, body={"text": text, "embedding": embedding})

# Search for documents by vector similarity
def search_documents(query_text, top_k=5, threshold=0.8):
    # Placeholder for query vector encoding
    query_embedding = encode_text(query_text)

    body = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, doc['embedding']) + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        }
    }

    results = es.search(index="documents", body=body)
    return results['hits']['hits']

# Placeholder for text encoding (you can use Sentence-BERT or another encoder)
def encode_text(text):
    return [0.1, 0.2, 0.3]  # Replace this with actual vector embedding
