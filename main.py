from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import logging
import re
import json

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
async def fetch_episode_data(query: str):
    url = f"https://yasdownloads.org/{query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch the page")

            soup = BeautifulSoup(response.text, "html.parser")
            script_tags = soup.find_all("script")

            for script in script_tags:
                if "window.seasonData" in script.text:
                    match = re.search(r'window\.seasonData\s*=\s*({.*?});', script.text, re.DOTALL)
                    if match:
                        season_data = json.loads(match.group(1))
                        return season_data

            return {"message": "No Hindi episode available"}

        except Exception as e:
            logger.error(f"Error fetching episode data: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# Vercel ASGI handler
from mangum import Mangum
handler = Mangum(app)
