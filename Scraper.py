import aiohttp
from bs4 import BeautifulSoup
import asyncio
from Search import index_document
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

async def scrape_news():
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get("https://timesofindia.indiatimes.com/") as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                articles = soup.find_all("a", class_="storylink")
                
                for i, article in enumerate(articles[:10]):
                    title = article.text
                    url = article['href']

                    embedding = encode_text(title)
                    await index_document(f"news_{i}", title, embedding)
                    print(f"Stored article: {title}")

            await asyncio.sleep(3600) 

def encode_text(text):
    embedding = model.encode(text)
    return embedding.tolist()
