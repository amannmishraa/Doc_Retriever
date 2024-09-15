from fastapi import FastAPI, HTTPException
from models import SearchRequest, Document
from database import initialize_index, index_document, delete_document, search_document
from cache import increment_user_requests, get_user_requests
from Scraper import scrape_news
import time
import asyncio

app = FastAPI(title="Document Retrieval System", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await initialize_index()
    asyncio.create_task(scrape_news()) 

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.post("/search")
async def search(request: SearchRequest):
    start_time = time.time()

    user_requests = await get_user_requests(request.user_id)
    if user_requests >= 5:
        raise HTTPException(status_code=429, detail="Too many requests")

    await increment_user_requests(request.user_id)

    try:
        results = await search_document(request.dict()) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    end_time = time.time()
    inference_time = end_time - start_time

    return {"results": results, "inference_time": inference_time}

@app.post("/ingest")
async def ingest_document(document: Document):
    try:
        doc_id = await index_document(document.dict())
        return {"message": "Document ingested successfully", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting document: {str(e)}")

@app.delete("/delete/{doc_id}")
async def delete_document_endpoint(doc_id: str):
    try:
        deleted = await delete_document(doc_id)
        if deleted:
            return {"message": "Document deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
