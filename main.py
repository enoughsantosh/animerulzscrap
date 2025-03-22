from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers)

        # Check for HTTP errors
        response.raise_for_status()

    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch data due to network issue.")

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch data from source.")

    soup = BeautifulSoup(response.text, "html.parser")

    # 🟢 Extract Spotlight
    def extract_spotlight():
        spotlight = []
        for slide in soup.select(".deslide-item"):
            try:
                title_elem = slide.select_one(".desi-head-title")
                image_elem = slide.select_one(".deslide-cover-img img")
                link_elem = slide.select_one(".desi-buttons a")

                if title_elem and image_elem and link_elem:
                    spotlight.append({
                        "title": title_elem.text.strip(),
                        "image": image_elem.get("data-src", ""),
                        "link": link_elem.get("href", ""),
                    })
            except Exception as e:
                logger.warning(f"Error extracting spotlight item: {e}")

        return spotlight

    # 🟢 Extract Trending
    def extract_trending():
        trending = []
        for item in soup.select("#trending-home .swiper-slide"):
            try:
                title_elem = item.select_one(".film-title")
                image_elem = item.select_one(".film-poster img")
                link_elem = item.select_one(".film-poster")

                if title_elem and image_elem and link_elem:
                    trending.append({
                        "title": title_elem.text.strip(),
                        "image": image_elem.get("data-src", ""),
                        "link": link_elem.get("href", ""),
                    })
            except Exception as e:
                logger.warning(f"Error extracting trending item: {e}")

        return trending

    # 🟢 Extract Anime from a Specific Section
    def extract_anime_by_section(section_title):
        anime_list = []
        try:
            section = soup.find("h2", string=section_title)
            if section:
                container = section.find_parent("section")
                if container:
                    for item in container.select(".film-poster"):
                        title_elem = item.select_one(".dynamic-name")
                        image_elem = item.select_one("img")
                        link_elem = item.select_one("a")

                        if title_elem and image_elem and link_elem:
                            anime_list.append({
                                "title": title_elem.text.strip(),
                                "image": image_elem.get("data-src", ""),
                                "link": link_elem.get("href", ""),
                            })
        except Exception as e:
            logger.warning(f"Error extracting section '{section_title}': {e}")

        return anime_list

    # 🟢 Extract Sections
    return {
        "Spotlight": extract_spotlight(),
        "Trending": extract_trending(),
        "Top Airing": extract_anime_by_section("Top Airing"),
        "Most Popular": extract_anime_by_section("Most Popular"),
        "Most Favourite": extract_anime_by_section("Most Favourite"),
        "Latest Completed": extract_anime_by_section("Latest Completed"),
    }
