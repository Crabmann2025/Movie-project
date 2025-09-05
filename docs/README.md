# Movie Manager 🎬

A simple Python app to manage your movie collection, fetch real movie data from the **OMDb API**, and generate a static website to showcase your movies.  

---

## Features

- Add movies by title – fetches data from OMDb API:
  - Title, Year, Rating, Poster image, IMDb ID
- List movies in your collection
- Delete movies
- Update movie rating & add notes
  - Notes can be attached to each movie
  - Notes are shown as a tooltip when hovering over the movie poster on the website
- Generate a static website (<username>.html) with all your movies
- Interactive website:
  - Click on poster → opens IMDb page in a new browser tab
  - Responsive grid layout → even with 20+ movies, the website stays clean and organized
- Random movie suggestion – pick a random movie from your collection
- Search movies – find a movie by title
- Movies sorted by rating – display movies in descending order of rating
- Multiple users support – each user has a separate collection
- Error handling – handles "movie not found", API connection issues, and missing template files gracefully

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Crabmann2025/Movie-project.git
2. Navigate to the project folder:
   ```bash 
   cd Movie-project
3. Install dependencies:
   ```bash  
   pip install -r requirements.txt
4. Create a .env file in the project root and add your API key:
   ```bash  
   API_KEY=your_api_key_here

---

## Setup

1. Get a free OMDb API key from OMDb API
2. Activate your API key via the link sent to your email
3. Insert your API key into the config.py file
   ```bash
   OMDB_API_KEY = "your_api_key_here"


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
After generating the website, a <username>.html file will be created in the generated_sites/ folder with your movie collection.

---

### Template Files
  - index_template.html – HTML template used for website generation
  - style.css – CSS styling for the website
    
### Template placeholders:
  - __TEMPLATE_TITLE__ – app title
  - __TEMPLATE_MOVIE_GRID__ – replaced with movie grid
  - __TEMPLATE_DATE__ – replaced with current date & time
  
---

## Database

- Uses SQLite (data/movies.db) to store users and movies
- Tables:
  - users → stores user names
  - movies → stores movie data including title, year, rating, poster, and notes

---

## Website Preview

✔️ Grid layout with posters
✔️ Hover for notes
✔️ Responsive design for all screen sizes

---

## Tests

- tests/test_movies.py
  - User creation & switching
  - Add, delete, update, and list movies
  - Random movie & search functionality
  - Website generation

- tests/test_movie_storage_sql.py
  - Database initialization (table creation)
  - Add & list users
  - Get user ID (existing & non-existing users)
  - Add & list movies
  - Update movie rating
  - Delete movie
  - Functions with non-existent users (graceful handling)

- Run tests:
  ```bash
  pytest tests/

  


