from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import init_db, SessionLocal, DocumentMetadata, UserRequest, encode_text
from cache import Cache
from typing import List
import time

app = FastAPI()

init_db()

cache = Cache()

class SearchRequest(BaseModel):
    text: str
    top_k: int = 5
    threshold: float = 0.5
    user_id: int

@app.on_event("startup")
def startup_event():
    pass

@app.get("/health")
async def health_check():
    return {"status": "API is active"}

@app.post("/search")
async def search(request: SearchRequest):
    # Check user request frequency
    db: Session = SessionLocal()
    user = db.query(UserRequest).filter(UserRequest.user_id == request.user_id).first()
    if user:
        user.request_count += 1
        if user.request_count > 5:
            raise HTTPException(status_code=429, detail="Too Many Requests")
        db.commit()
    else:
        new_user = UserRequest(user_id=request.user_id, request_count=1)
        db.add(new_user)
        db.commit()

    start_time = time.time()

    cache_key = f"search_{request.text}_{request.top_k}_{request.threshold}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    documents = db.query(DocumentMetadata).all()
    results = []
    for doc in documents:
        similarity_score = np.random.rand() 
        if similarity_score >= request.threshold:
            results.append({"title": doc.title, "description": doc.description, "score": similarity_score})

    results = sorted(results, key=lambda x: x["score"], reverse=True)[:request.top_k]

    result_to_cache = {"results": results, "inference_time": time.time() - start_time}
    cache.set(cache_key, result_to_cache)

    return result_to_cache
