import requests
from config import OMDB_API_KEY

BASE_URL = "https://www.omdbapi.com/"

def fetch_movie(title: str) -> dict:
    """Fetch movie details from OMDb including poster, safely handling special cases."""
    params = {"apikey": OMDB_API_KEY, "t": title}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error: Could not reach OMDb API. {e}")
        return {}

    if data.get("Response") == "False":
        print(f"Movie not found: {title}")
        return {}

    # --- Year ---
    year_str = data.get("Year", "0")
    try:
        # Nimmt nur die ersten 4 Ziffern
        year = int(''.join(filter(str.isdigit, year_str[:4])))
    except ValueError:
        year = 0

    # --- Rating ---
    imdb_rating = data.get("imdbRating", "0")
    try:
        rating = float(imdb_rating) if imdb_rating != "N/A" else 0.0
    except ValueError:
        rating = 0.0

    return {
        "title": data.get("Title", "Unknown"),
        "year": year,
        "rating": rating,
        "poster_url": data.get("Poster", "")
    }
