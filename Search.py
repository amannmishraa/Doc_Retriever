from elasticsearch import AsyncElasticsearch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Elasticsearch client
es = AsyncElasticsearch("http://elasticsearch:9200")

async def index_document(doc_id, text, embedding):
    try:
        response = await es.index(index="documents", id=doc_id, body={"text": text, "embedding": embedding})
        logger.info(f"Document indexed with response: {response}")
    except Exception as e:
        logger.error(f"Error indexing document: {e}")

async def search_documents(query_text, top_k=5, threshold=0.8):
    try:
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
        logger.info(f"Search results: {results}")
        return results['hits']['hits']
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return []

def encode_text(text):
    # Dummy embedding function
    return [0.1, 0.2, 0.3]

# Example usage
async def main():
    # Index a sample document
    await index_document("1", "Sample document text", [0.1, 0.2, 0.3])
    
    # Search for documents
    results = await search_documents("Sample query")
    logger.info(f"Search results: {results}")

# Run the example usage
import asyncio
asyncio.run(main())
