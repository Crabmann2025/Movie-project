# Movie Manager 🎬

A simple Python app to manage your movie collection, fetch real movie data from the **OMDb API**, and generate a static website to showcase your movies.  

---

## Features

- **Add movies by title** – fetches data from OMDb API:
  - Title, Year, Rating, Poster image, IMDb ID  
- **List movies** in your collection  
- **Delete movies**  
- **Update movie rating & add notes**  
  - Notes can be attached to each movie  
  - Notes are shown as a tooltip when hovering over the movie poster on the website  
- **Generate a static website** (`<username>.html`) with all your movies  
- **Interactive website**:
  - Hover over poster → see your personal movie note  
  - Click on poster → opens IMDb page in a new browser tab  
  - Responsive grid layout → even with 20+ movies, the website stays clean and organized  
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
3. Insert your API key into the config.py file

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
  4. Update movie (rating + notes)
  5. Stats
  6. Random movie
  7. Search movie
  8. Movies sorted by rating
  9. Generate website
  10. Switch user
After generating the website, a <username>.html file will be created with your movie collection.

---

### Template Files
  - index_template.html – HTML template used for website generation
  - style.css – CSS styling for the website
### Template placeholders:
  - __TEMPLATE_TITLE__ – app title
  - __TEMPLATE_MOVIE_GRID__ – replaced with movie grid
  
---

## Website Preview

✔️ Grid layout with posters
✔️ Hover for notes
