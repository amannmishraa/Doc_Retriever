# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time
import logging
import threading
from Search import search_documents
from Scraper import scrape_news
from cache import cache_results, get_cached_results

app = FastAPI()

user_requests = {}

logging.basicConfig(filename='app.log', level=logging.INFO)

@app.get("/health")
def health_check():
    return {"status": "API is active"}

class SearchQuery(BaseModel):
    text: str
    top_k: int = 5
    threshold: float = 0.8
    user_id: str

@app.post("/search")
def search(query: SearchQuery):
    if query.user_id in user_requests and user_requests[query.user_id] >= 5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    start_time = time.time()

    cached_results = get_cached_results(query.user_id)
    if cached_results:
        results = cached_results
    else:
        results = search_documents(query.text, query.top_k, query.threshold)
        cache_results(query.user_id, results)
    
    if query.user_id not in user_requests:
        user_requests[query.user_id] = 0
    user_requests[query.user_id] += 1

    inference_time = time.time() - start_time
    logging.info(f"User: {query.user_id}, Inference time: {inference_time:.4f}s")

    return {"results": results, "inference_time": inference_time}

threading.Thread(target=scrape_news).start()
