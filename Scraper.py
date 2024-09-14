import threading
import requests
from bs4 import BeautifulSoup
import time

def scrape_news():
    while True:
        response = requests.get("https://timesofindia.indiatimes.com/")
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("a", class_="storylink")
        for article in articles[:10]:
            print(article.text)  
        time.sleep(3600)  

threading.Thread(target=scrape_news).start()