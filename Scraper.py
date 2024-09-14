import requests
from bs4 import BeautifulSoup
import time
from Search import index_document
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
def scrape_news():
    while True:
        response = requests.get("https://timesofindia.indiatimes.com/")
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("a", class_="storylink")
        
        for i, article in enumerate(articles[:10]):
            title = article.text
            url = article['href']
            
            embedding = encode_text(title)
            
            index_document(f"news_{i}", title, embedding)
            print(f"Stored article: {title}")
        time.sleep(3600)

def encode_text(text):
    embedding = model.encode(text) 
    return embedding.tolist() 
