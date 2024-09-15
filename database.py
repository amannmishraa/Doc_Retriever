from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel
from typing import Dict, Any

es = AsyncElasticsearch("http://elasticsearch:9200")
ELASTICSEARCH_INDEX = "documents"

class Document(BaseModel):
    title: str
    content: str

async def initialize_index():
    exists = await es.indices.exists(index=ELASTICSEARCH_INDEX)
    if not exists:
        await es.indices.create(index=ELASTICSEARCH_INDEX)

async def index_document(document: Dict[str, Any]) -> str:
    try:
        response = await es.index(index=ELASTICSEARCH_INDEX, document=document)
        return response['_id']
    except Exception as e:
        raise RuntimeError(f"Failed to index document: {e}")

async def delete_document(doc_id: str) -> bool:
    try:
        response = await es.delete(index=ELASTICSEARCH_INDEX, id=doc_id)
        return response['result'] == 'deleted'
    except Exception as e:
        raise RuntimeError(f"Failed to delete document: {e}")

async def search_document(query: Dict[str, Any]) -> Dict[str, Any]:
    try:
        response = await es.search(index=ELASTICSEARCH_INDEX, query=query)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to search documents: {e}")
