import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def scrape_news():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get("https://timesofindia.indiatimes.com/") as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        
                        articles = soup.find_all("a", class_="hpKNW")
                        
                        for article in articles:
                            title = article.get_text(strip=True)
                            link = article.get("href")
                            
                            if link and link.startswith("/"):
                                link = "https://timesofindia.indiatimes.com" + link
                            
                            if title and link:
                                logger.info(f"Title: {title}, Link: {link}")
                        
                    else:
                        logger.error(f"Failed to fetch news. Status code: {response.status}")

            except Exception as e:
                logger.error(f"An error occurred: {e}")

            await asyncio.sleep(3600) 
from elasticsearch import Elasticsearch

es = Elasticsearch("http://elasticsearch:9200")

async def scrape_news():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get("https://timesofindia.indiatimes.com/") as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        articles = soup.find_all("a", class_="hpKNW")  

                        for article in articles:
                            title = article.get_text(strip=True)
                            link = article.get("href")
                            logger.info(f"Title: {title}, Link: {link}")

                            # Indexing to Elasticsearch
                            es.index(index="documents", document={"title": title, "link": link})
                        
                    else:
                        logger.error(f"Failed to fetch news. Status code: {response.status}")

            except Exception as e:
                logger.error(f"An error occurred: {e}")

            await asyncio.sleep(3600)  


if __name__ == "__main__":
    asyncio.run(scrape_news())

