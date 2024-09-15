from elasticsearch import AsyncElasticsearch

es = es = AsyncElasticsearch("http://elasticsearch:9200")


async def index_document(doc_id, text, embedding):
    await es.index(index="documents", id=doc_id, body={"text": text, "embedding": embedding})

async def search_documents(query_text, top_k=5, threshold=0.8):
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

    results = await es.search(index="documents", body=body)
    return results['hits']['hits']

def encode_text(text):
    return [0.1, 0.2, 0.3]
