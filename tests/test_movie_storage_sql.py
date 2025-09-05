import pytest
from sqlalchemy import create_engine, text

import movie_storage_sql as storage


# Fixture: In-Memory DB
@pytest.fixture
def in_memory_db(monkeypatch):
    # Erstelle temporäre SQLite In-Memory-Engine
    engine = create_engine("sqlite:///:memory:", echo=False)
    monkeypatch.setattr(storage, "engine", engine)
    storage.init_db()
    return engine


# Test init_db
def test_init_db_creates_tables(in_memory_db):
    with in_memory_db.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
        table_names = [row[0] for row in result]
        assert "users" in table_names
        assert "movies" in table_names


# Test add_user & list_users
def test_add_and_list_user(in_memory_db):
    storage.add_user("Alice")
    users = storage.list_users()
    assert "Alice" in users


# Test get_user_id
def test_get_user_id(in_memory_db):
    storage.add_user("Bob")
    user_id = storage.get_user_id("Bob")
    assert user_id is not None
    # Nicht vorhandener User
    assert storage.get_user_id("NoUser") is None


# Test add_movie & list_movies
def test_add_and_list_movie(in_memory_db):
    storage.add_user("TestUser")
    storage.add_movie("Movie1", 2020, 7.5, poster_url="poster1.jpg", user="TestUser")
    movies = storage.list_movies("TestUser")
    assert any(m["title"] == "Movie1" for m in movies.values())


# Test update_movie
def test_update_movie_rating(in_memory_db):
    storage.add_user("TestUser")
    storage.add_movie("Movie2", 2021, 6.0, user="TestUser")
    movies = storage.list_movies("TestUser")
    movie_id = list(movies.keys())[0]
    storage.update_movie(movie_id, 9.0, user="TestUser")
    updated_movies = storage.list_movies("TestUser")
    assert updated_movies[movie_id]["rating"] == 9.0


# Test delete_movie
def test_delete_movie(in_memory_db):
    storage.add_user("TestUser")
    storage.add_movie("Movie3", 2022, 8.0, user="TestUser")
    movies = storage.list_movies("TestUser")
    movie_id = list(movies.keys())[0]
    storage.delete_movie(movie_id, user="TestUser")
    updated_movies = storage.list_movies("TestUser")
    assert movie_id not in updated_movies


# Test movie functions with non-existent user
def test_movie_for_nonexistent_user(in_memory_db):
    assert storage.get_user_id("NoUser") is None
    assert storage.list_movies("NoUser") == {}
    # update_movie & delete_movie sollten nichts tun und keine Exception werfen
    storage.update_movie(1, 5.0, user="NoUser")
    storage.delete_movie(1, user="NoUser")
