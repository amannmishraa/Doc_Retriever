from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

def index_document(doc_id, text, embedding):
    es.index(index="documents", id=doc_id, body={"text": text, "embedding": embedding})

def search_documents(query_text, top_k=5, threshold=0.8):
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

def encode_text(text):
    return [0.1, 0.2, 0.3] 
