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

    # 🟢 Extract Other Sections (Top Airing, Most Popular, Most Favourite, Latest Completed)
    def extract_section(section_class):
        anime_list = []
        section = soup.select_one(f".{section_class}")  # Corrected selector

        if section:
            for item in section.select(".film-poster"):
                title_elem = item.select_one(".dynamic-name")
                image_elem = item.select_one("img")
                link_elem = item.select_one("a")

                if title_elem and image_elem and link_elem:
                    anime_list.append({
                        "title": title_elem.text.strip(),
                        "image": image_elem["data-src"],
                        "link": link_elem["href"],
                    })
        return anime_list

    # Corrected section class names from the HTML
    top_airing = extract_section("block_area_top-airing")
    most_popular = extract_section("block_area_most-popular")
    most_favourite = extract_section("block_area_most-favourite")
    latest_completed = extract_section("block_area_latest-completed")

    return {
        "Spotlight": extract_spotlight(),
        "Trending": extract_trending(),
        "Top Airing": top_airing,
        "Most Popular": most_popular,
        "Most Favourite": most_favourite,
        "Latest Completed": latest_completed,
    }
