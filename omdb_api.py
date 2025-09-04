import requests
from config import OMDB_API_KEY

BASE_URL = "https://www.omdbapi.com/"

def fetch_movie(title: str) -> dict:
    """Fetch movie details from OMDb including poster."""
    params = {"apikey": OMDB_API_KEY, "t": title}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        print("Error: Could not reach OMDb API.")
        return {}

    if data.get("Response") == "False":
        print(f"Movie not found: {title}")
        return {}

    return {
        "title": data.get("Title"),
        "year": int(data.get("Year", 0)),
        "rating": float(data.get("imdbRating", 0)) if data.get("imdbRating") != "N/A" else 0.0,
        "poster_url": data.get("Poster", "")
    }
