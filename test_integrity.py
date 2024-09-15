# test_data_integrity.py
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def test_data_integrity():
    # Index a sample document
    doc_id = 2
    document = {"title": "Integrity Test", "link": "https://timesofindia.indiatimes.com/"}
    es.index(index="documents_v2", id=doc_id, body=document)
    
    # Retrieve and verify document
    response = es.get(index="documents_v2", id=doc_id)
    assert response['_source']['title'] == "Integrity Test", "Title does not match"
    assert response['_source']['link'] == "https://timesofindia.indiatimes.com/", "Link does not match"

test_data_integrity()
