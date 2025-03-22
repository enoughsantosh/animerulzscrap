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

@app.get("/home")
async def fetch_homepage():
    url = "https://animerulzapp.com/home"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data")

    soup = BeautifulSoup(response.text, "html.parser")

    def extract_spotlight():
        spotlight = []
        for slide in soup.select(".deslide-item"):
            title_elem = slide.select_one(".desi-head-title")
            image_elem = slide.select_one(".deslide-cover-img img")
            link_elem = slide.select_one(".desi-buttons a")

            if title_elem and image_elem and link_elem:
                spotlight.append({
                    "title": title_elem.text.strip(),
                    "image": image_elem["data-src"],
                    "link": link_elem["href"],
                })
        return spotlight

    def extract_trending():
        trending = []
        for item in soup.select("#trending-home .swiper-slide"):
            title_elem = item.select_one(".film-title")
            image_elem = item.select_one(".film-poster img")
            link_elem = item.select_one(".film-poster")

            if title_elem and image_elem and link_elem:
                trending.append({
                    "title": title_elem.text.strip(),
                    "image": image_elem["data-src"],
                    "link": link_elem["href"],
                })
        return trending

    # Placeholder for missing categories
    def extract_top_airing(): return []
    def extract_most_popular(): return []
    def extract_most_favourite(): return []
    def extract_latest_completed(): return []

    return {
        "Spotlight": extract_spotlight(),
        "Trending": extract_trending(),
        "Top Airing": extract_top_airing(),
        "Most Popular": extract_most_popular(),
        "Most Favourite": extract_most_favourite(),
        "Latest Completed": extract_latest_completed(),
    }
