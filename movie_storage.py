# movie_storage.py
import json

FILENAME = "movies.json"

def get_movies():
    """Lädt alle Filme aus der Datei."""
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_movies(movies):
    """Speichert alle Filme in die Datei."""
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4)

def add_movie(title, year, rating):
    """Fügt einen neuen Film hinzu."""
    movies = get_movies()
    if title in movies:
        raise ValueError(f"Film '{title}' existiert bereits.")
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)

def delete_movie(title):
    """Löscht einen Film."""
    movies = get_movies()
    if title not in movies:
        raise ValueError(f"Film '{title}' nicht gefunden.")
    del movies[title]
    save_movies(movies)

def update_movie(title, new_rating):
    """Aktualisiert die Bewertung eines Films."""
    movies = get_movies()
    if title not in movies:
        raise ValueError(f"Film '{title}' nicht gefunden.")
    movies[title]['rating'] = new_rating
    save_movies(movies)