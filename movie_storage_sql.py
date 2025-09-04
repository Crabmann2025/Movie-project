from sqlalchemy import create_engine, text

# Database URL
DB_URL = "sqlite:///movies.db"

# Create engine
engine = create_engine(DB_URL, echo=False)

# Create "movies" table if it doesn't exist
with engine.connect() as conn_outer:
    conn_outer.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT
        )
    """))
    conn_outer.commit()


def list_movies():
    """Return all movies as a dictionary."""
    with engine.connect() as conn_inner:
        result = conn_inner.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()
    return {
        row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]}
        for row in movies
    }


def add_movie(title, year, rating, poster_url=None):
    """Add a new movie to the database."""
    with engine.connect() as conn_inner:
        try:
            conn_inner.execute(text(
                "INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"
            ), {"title": title, "year": year, "rating": rating, "poster_url": poster_url})
            conn_inner.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error adding movie '{title}': {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as conn_inner:
        try:
            result = conn_inner.execute(text(
                "DELETE FROM movies WHERE title = :title"
            ), {"title": title})
            conn_inner.commit()
            if result.rowcount:
                print(f"Movie '{title}' deleted successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error deleting movie '{title}': {e}")


def update_movie(title, rating):
    """Update the rating of a movie."""
    with engine.connect() as conn_inner:
        try:
            result = conn_inner.execute(text(
                "UPDATE movies SET rating = :rating WHERE title = :title"
            ), {"title": title, "rating": rating})
            conn_inner.commit()
            if result.rowcount:
                print(f"Movie '{title}' updated successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error updating movie '{title}': {e}")


