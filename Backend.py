from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

user_requests = {}

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

    results = [{"document": "Document 1", "similarity": 0.9}, {"document": "Document 2", "similarity": 0.85}]

    if query.user_id not in user_requests:
        user_requests[query.user_id] = 0
    user_requests[query.user_id] += 1

    inference_time = time.time() - start_time
    print(f"Inference time: {inference_time:.4f} seconds")
    
    return {"results": results[:query.top_k], "inference_time": inference_time}
