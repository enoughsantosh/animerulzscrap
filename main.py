from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend access
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

    # 🟢 Extract Spotlight
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

    # 🟢 Extract Trending
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

    # 🟢 Extract Top Airing
    def extract_top_airing():
        top_airing = []
        for item in soup.select('.block_area:has(h2:contains("Top Airing")) .film-poster'):
            title_elem = item.select_one(".dynamic-name")
            image_elem = item.select_one("img")
            link_elem = item.select_one("a")

            if title_elem and image_elem and link_elem:
                top_airing.append({
                    "title": title_elem.text.strip(),
                    "image": image_elem["data-src"],
                    "link": link_elem["href"],
                })
        return top_airing

    # 🟢 Extract Most Popular
    def extract_most_popular():
        most_popular = []
        for item in soup.select('.block_area:has(h2:contains("Most Popular")) .film-poster'):
            title_elem = item.select_one(".dynamic-name")
            image_elem = item.select_one("img")
            link_elem = item.select_one("a")

            if title_elem and image_elem and link_elem:
                most_popular.append({
                    "title": title_elem.text.strip(),
                    "image": image_elem["data-src"],
                    "link": link_elem["href"],
                })
        return most_popular

    # 🟢 Extract Most Favourite
    def extract_most_favourite():
        most_favourite = []
        for item in soup.select('.block_area:has(h2:contains("Most Favourite")) .film-poster'):
            title_elem = item.select_one(".dynamic-name")
            image_elem = item.select_one("img")
            link_elem = item.select_one("a")

            if title_elem and image_elem and link_elem:
                most_favourite.append({
                    "title": title_elem.text.strip(),
                    "image": image_elem["data-src"],
                    "link": link_elem["href"],
                })
        return most_favourite

    # 🟢 Extract Latest Completed
    def extract_latest_completed():
        latest_completed = []
        for item in soup.select('.block_area:has(h2:contains("Latest Completed")) .film-poster'):
            title_elem = item.select_one(".dynamic-name")
            image_elem = item.select_one("img")
            link_elem = item.select_one("a")

            if title_elem and image_elem and link_elem:
                latest_completed.append({
                    "title": title_elem.text.strip(),
                    "image": image_elem["data-src"],
                    "link": link_elem["href"],
                })
        return latest_completed

    return {
        "Spotlight": extract_spotlight(),
        "Trending": extract_trending(),
        "Top Airing": extract_top_airing(),
        "Most Popular": extract_most_popular(),
        "Most Favourite": extract_most_favourite(),
        "Latest Completed": extract_latest_completed(),
    }
