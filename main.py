from fastapi import FastAPI, Query, HTTPException
import requests
import httpx
from urllib.parse import urlparse
from pydantic import BaseModel
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Anime Search API is running!"}
# Homepage 
@app.get("/home")

def handler(event, context):
    url = "https://animerulzapp.com/home"
    headers = {"User-Agent": "Mozilla/5.0"}

    # Fetch HTML
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    def extract_spotlight():
        spotlight = []
        for slide in soup.select(".deslide-item"):
            title = slide.select_one(".desi-head-title").text.strip()
            image = slide.select_one(".deslide-cover-img img")["data-src"]
            link = slide.select_one(".desi-buttons a")["href"]
            spotlight.append({"title": title, "image": image, "link": link})
        return spotlight

    def extract_trending():
        trending = []
        for item in soup.select("#trending-home .swiper-slide"):
            title = item.select_one(".film-title").text.strip()
            image = item.select_one(".film-poster img")["data-src"]
            link = item.select_one(".film-poster")["href"]
            trending.append({"title": title, "image": image, "link": link})
        return trending

    # Placeholder for other categories
    def extract_top_airing():
        return []

    def extract_most_popular():
        return []

    def extract_most_favourite():
        return []

    def extract_latest_completed():
        return []

    data = {
        "Spotlight": extract_spotlight(),
        "Trending": extract_trending(),
        "Top Airing": extract_top_airing(),
        "Most Popular": extract_most_popular(),
        "Most Favourite": extract_most_favourite(),
        "Latest Completed": extract_latest_completed(),
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data, ensure_ascii=False, indent=4),
    }
