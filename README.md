# Movie Manager 🎬

A simple Python app to manage your movie collection, fetch real movie data from the **OMDb API**, and generate a static website to showcase your movies.  

---

## Features

- **Add movies by title** – fetches data from OMDb API:
                          - Title, Year, Rating, Poster image
- **List movies** in your collection
- **Delete movies**
- **Generate a static website** (`index.html`) with all your movies
- **Error handling**: handles "movie not found" and API connection issues gracefully  

---

## Requirements

- Install the required packages:
  ```bash
  pip install -r requirements.txt

---

## Setup

1. Get a free OMDb API key from OMDb API
2. Activate your API key via the link sent to your email
3. Insert your API key into the application configuration

---

## Usage

- Run the app:
  ```bash
  python main.py

- Menu options:
  ```bash
  0. Exit
  1. List movies
  2. Add movie
  3. Delete movie
  4. Update movie
  5. Stats
  6. Random movie
  7. Search movie
  8. Movies sorted by rating
  9. Generate website
After generating the website, an index.html file will be created with your movie collection.

---

### Template Files

- index_template.html – HTML template used for website generation
- style.css – CSS styling for the website

### Template placeholders:

- __TEMPLATE_TITLE__ – app title
- __TEMPLATE_MOVIE_GRID__ – replaced with movie grid

### Code Quality

- Modular and clean code
- Follows PEP 8 guidelines
- Easy to maintain and extend

---
