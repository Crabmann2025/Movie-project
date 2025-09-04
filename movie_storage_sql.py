from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the "movies" table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT
        )
    """))
    connection.commit()


def list_movies():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()
    return {
        row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]}
        for row in movies
    }



def add_movie(title, year, rating, poster_url=None):
    with engine.connect() as connection:
        try:
            connection.execute(text(
                "INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"
            ), {"title": title, "year": year, "rating": rating, "poster_url": poster_url})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text(
                "DELETE FROM movies WHERE title = :title"
            ), {"title": title})
            connection.commit()
            if result.rowcount:
                print(f"Movie '{title}' deleted successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text(
                "UPDATE movies SET rating = :rating WHERE title = :title"
            ), {"title": title, "rating": rating})
            connection.commit()
            if result.rowcount:
                print(f"Movie '{title}' updated successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error: {e}")

# Optional: quick test block
if __name__ == "__main__":
    # Example data
    add_movie("Inception", 2010, 8.8)
    print(list_movies())
    update_movie("Inception", 9.0)
    print(list_movies())
    delete_movie("Inception")
    print(list_movies())
