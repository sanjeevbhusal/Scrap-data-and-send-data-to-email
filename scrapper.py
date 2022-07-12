from bs4 import BeautifulSoup
import requests
from pprint import pprint

def get_html():
    return requests.get("https://news.ycombinator.com/news").text

def get_filtered_news(soup):
    news_list = soup.select(".athing")
    filtered_news = []
    for news in news_list:
        title = news.select(".titlelink")[0].string
        link = news.select(".titlelink")[0].get("href")
        votes = int(news.nextSibling.select(".score")[0].string.replace(" points", ""))
        if votes >= 100:
            filtered_news.append({"title": title, "votes": votes, "link" : link})
            
    return filtered_news

def scrape_news_list():
    html = get_html()
    soup = BeautifulSoup(html, "html.parser")
    filtered_news = get_filtered_news(soup)      
    return sorted(filtered_news, key=lambda k: k['votes'], reverse=True)

    
if __name__ == "__main__":
    pprint(scrape_news_list())