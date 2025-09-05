# movie_storage_sql.py
from sqlalchemy import create_engine, text

DB_URL = "sqlite:///data/movies.db"
engine = create_engine(DB_URL, echo=False)

# Create tables if they don't exist
def init_db():
    with engine.connect() as connection:
        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
        """))
        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """))
        connection.commit()


#  User Functions
def list_users():
    """Return a list of all users."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT username FROM users"))
        return [row[0] for row in result.fetchall()]

def add_user(username):
    """Create a new user."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO users (username) VALUES (:username)"),
                {"username": username}
            )
            connection.commit()
            print(f"User '{username}' created successfully.")
        except Exception as e:
            print(f"Error creating user: {e}")


def get_user_id(username):
    """Return the user ID for a given username."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id FROM users WHERE username=:username"),
            {"username": username}
        ).fetchone()
    return result[0] if result else None


#  Movie Functions
def list_movies(username):
    """Return all movies for a user as a dict keyed by movie ID."""
    user_id = get_user_id(username)
    if not user_id:
        return {}

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, title, year, rating, poster_url FROM movies WHERE user_id=:user_id"),
            {"user_id": user_id}
        ).fetchall()

    return {row[0]: {"title": row[1], "year": row[2], "rating": row[3], "poster_url": row[4]} for row in result}


def add_movie(title, year, rating, poster_url=None, user=None):
    """Add a movie for a user."""
    user_id = get_user_id(user)
    if not user_id:
        print(f"User '{user}' not found.")
        return

    with engine.connect() as connection:
        try:
            connection.execute(
                text("""
                    INSERT INTO movies (title, year, rating, poster_url, user_id)
                    VALUES (:title, :year, :rating, :poster_url, :user_id)
                """),
                {"title": title, "year": year, "rating": rating, "poster_url": poster_url, "user_id": user_id}
            )
            connection.commit()
            print(f"Movie '{title}' added for {user}.")
        except Exception as e:
            print(f"Error adding movie: {e}")


def delete_movie(movie_id, user=None):
    """Delete a movie by its ID for a specific user."""
    user_id = get_user_id(user)
    if not user_id:
        print(f"User '{user}' not found.")
        return

    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE id=:id AND user_id=:user_id"),
            {"id": movie_id, "user_id": user_id}
        )
        connection.commit()
        if result.rowcount:
            print(f"Movie ID {movie_id} deleted for {user}.")
        else:
            print(f"Movie ID {movie_id} not found for {user}.")


def update_movie(movie_id, rating, user=None):
    """Update a movie's rating by ID for a specific user."""
    user_id = get_user_id(user)
    if not user_id:
        print(f"User '{user}' not found.")
        return

    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating=:rating WHERE id=:id AND user_id=:user_id"),
            {"rating": rating, "id": movie_id, "user_id": user_id}
        )
        connection.commit()
        if result.rowcount:
            print(f"Movie ID {movie_id} rating updated for {user}.")
        else:
            print(f"Movie ID {movie_id} not found for {user}.")

if __name__ == "__main__":
    init_db()
