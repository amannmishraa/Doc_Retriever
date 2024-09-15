# test_search.py
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def test_search_documents():

    es.index(index="documents_v2", id=1, body={"title": "Sample Document", "link": "https://timesofindia.indiatimes.com/"})
    
    body = {
        "query": {
            "match": {
                "title": "Sample"
            }
        }
    }
    response = es.search(index="documents_v2", body=body)
    
    assert len(response['hits']['hits']) > 0, "No results found"
    assert response['hits']['hits'][0]['_source']['title'] == "Sample Document", "Title does not match"

test_search_documents()
