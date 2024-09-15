from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import logging
import asyncio
from Scraper import scrape_news  

app = FastAPI()
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

user_request_count = {}
USER_REQUEST_LIMIT = 5

async def scrape_news_task():
    while True:
        try:
            await scrape_news()
        except Exception as e:
            logger.error(f"Failed to scrape news: {e}")
        await asyncio.sleep(3600) 

@app.on_event("startup")
async def startup_event():
    logger.info("Starting background news scraping task...")
    asyncio.create_task(scrape_news_task()) 

@app.get("/health")
async def health_check():
    return {"status": "ok"}

class SearchRequest(BaseModel):
    text: str
    top_k: int = 10
    threshold: float = 0.7
    user_id: str

@app.post("/search")
async def search(request: SearchRequest):
    user_id = request.user_id
    if user_id not in user_request_count:
        user_request_count[user_id] = 1
    else:
        user_request_count[user_id] += 1
    
    if user_request_count[user_id] > USER_REQUEST_LIMIT:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    logger.info(f"Search request by user {user_id}: text={request.text}, top_k={request.top_k}, threshold={request.threshold}")
    results = {
        "results": [
            {"id": 1, "title": "Sample Result 1"},
            {"id": 2, "title": "Sample Result 2"}
        ]
    }
    return results

