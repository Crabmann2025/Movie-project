import os
import re
import random
import pytest
from unittest.mock import patch, mock_open

# Mock DB when importing movies.py
with patch("movie_storage_sql.init_db"), \
     patch("movie_storage_sql.list_movies"), \
     patch("movie_storage_sql.add_movie"), \
     patch("movie_storage_sql.update_movie"), \
     patch("movie_storage_sql.delete_movie"), \
     patch("movie_storage_sql.list_users"), \
     patch("movie_storage_sql.add_user"):
    import movies  # The file you want to test


# Fixture: reset active_user
@pytest.fixture(autouse=True)
def reset_active_user():
    movies.active_user = None
    yield
    movies.active_user = None


# Tests get_user_movies
def test_get_user_movies_no_user():
    movies.active_user = None
    result = movies.get_user_movies()
    assert result == {}


@patch("movie_storage_sql.list_movies")
def test_get_user_movies_with_user(mock_list):
    movies.active_user = "TestUser"
    mock_list.return_value = {"1": {"title": "TestMovie", "year": 2020, "rating": 8.0}}
    result = movies.get_user_movies()
    assert "1" in result
    assert result["1"]["title"] == "TestMovie"


# Tests choose_user
@patch("builtins.input", side_effect=["2"])
@patch("movie_storage_sql.list_users", return_value=["User1", "User2"])
@patch("movie_storage_sql.add_user")
def test_choose_user_existing(mock_add, mock_users, mock_input):
    movies.choose_user()
    assert movies.active_user == "User2"


@patch("builtins.input", side_effect=["3", "NewUser"])
@patch("movie_storage_sql.list_users", return_value=["User1", "User2"])
@patch("movie_storage_sql.add_user")
def test_choose_user_new(mock_add, mock_users, mock_input):
    movies.choose_user()
    assert movies.active_user == "NewUser"
    mock_add.assert_called_once_with("NewUser")


# Test add_movie
@patch("builtins.input", side_effect=["TestMovie"])
@patch("movies.fetch_movie")
@patch("movie_storage_sql.add_movie")
def test_add_movie(mock_add_movie, mock_fetch, mock_input):
    movies.active_user = "TestUser"
    mock_fetch.return_value = {"title": "TestMovie", "year": 2020, "rating": 8.0, "poster_url": ""}
    movies.add_movie()
    mock_add_movie.assert_called_once()


# Test select_movie
@patch("movies.get_numeric_input", return_value=1)
@patch("movies.get_user_movies")
def test_select_movie(mock_get_movies, mock_input):
    movies.active_user = "TestUser"
    mock_get_movies.return_value = {"1": {"title": "Movie1", "year": 2020, "rating": 7.0}}
    movie_id, movie = movies.select_movie()
    assert movie_id == "1"
    assert movie["title"] == "Movie1"


# Test delete_movie
@patch("movies.select_movie", return_value=("1", {"title": "Movie1"}))
@patch("movie_storage_sql.delete_movie")
def test_delete_movie(mock_delete, mock_select):
    movies.active_user = "TestUser"
    movies.delete_movie()
    mock_delete.assert_called_once_with("1", user="TestUser")


# Test update_movie_rating
@patch("movies.select_movie", return_value=("1", {"title": "Movie1"}))
@patch("movies.get_numeric_input", return_value=9.5)
@patch("movie_storage_sql.update_movie")
def test_update_movie_rating(mock_update, mock_input, mock_select):
    movies.active_user = "TestUser"
    movies.update_movie_rating()
    mock_update.assert_called_once_with("1", 9.5, user="TestUser")


# Test movies_sorted_by_rating
@patch("movies.get_user_movies")
def test_movies_sorted_by_rating(mock_get_movies, capsys):
    movies.active_user = "TestUser"
    mock_get_movies.return_value = {
        "1": {"title": "A", "year": 2020, "rating": 5},
        "2": {"title": "B", "year": 2021, "rating": 8},
    }
    movies.movies_sorted_by_rating()
    captured = capsys.readouterr()
    assert "B" in captured.out.splitlines()[1]


# Test search_movies
@patch("movies.get_user_movies")
@patch("builtins.input", side_effect=["Movie1"])
def test_search_movies_found(mock_input, mock_get_movies, capsys):
    movies.active_user = "TestUser"
    mock_get_movies.return_value = {"1": {"title": "Movie1", "year": 2020, "rating": 7.0}}
    movies.search_movies()
    captured = capsys.readouterr()
    assert "Movie1" in captured.out


# Test random_movie
@patch("movies.get_user_movies")
def test_random_movie(mock_get_movies, capsys):
    movies.active_user = "TestUser"
    mock_get_movies.return_value = {"1": {"title": "Movie1", "year": 2020, "rating": 7.0}}
    random.seed(0)
    movies.random_movie()
    captured = capsys.readouterr()
    assert "Movie1" in captured.out


# Test generate_website
@patch("os.path.exists", return_value=True)  # Template exists
@patch("movies.storage.list_movies")
@patch("os.makedirs")
@patch("builtins.open", new_callable=mock_open,
       read_data="__TEMPLATE_TITLE__ __TEMPLATE_MOVIE_GRID__ __TEMPLATE_DATE__")
def test_generate_website_success(mock_file, mock_makedirs, mock_list_movies, mock_exists):
    movies.active_user = "TestUser"
    mock_list_movies.return_value = {
        "1": {"title": "Movie1", "year": 2020, "rating": 7.0, "poster_url": "poster1.jpg"}
    }

    movies.generate_website()

    # Check directories created
    mock_makedirs.assert_called_once_with("generated_sites", exist_ok=True)

    # Check file was written
    mock_file.assert_called_with(os.path.join("generated_sites", "TestUser.html"), "w", encoding="utf-8")

    handle = mock_file()
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    assert "TestUser's Movie Library" in written_content
    assert "Movie1" in written_content
    assert "poster1.jpg" in written_content
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", written_content)


# Test generate_website with no active user
def test_generate_website_no_user(capsys):
    movies.active_user = None
    movies.generate_website()
    captured = capsys.readouterr()
    assert "No active user selected" in captured.out


# Test generate_website with missing template
@patch("os.path.exists", return_value=False)
def test_generate_website_no_template(mock_exists, capsys):
    movies.active_user = "TestUser"
    movies.generate_website()
    captured = capsys.readouterr()
    assert "Template file not found" in captured.out


# Test generate_website with no movies
@patch("os.path.exists", return_value=True)
@patch("movies.storage.list_movies", return_value={})
@patch("builtins.open", new_callable=mock_open,
       read_data="__TEMPLATE_TITLE__ __TEMPLATE_MOVIE_GRID__ __TEMPLATE_DATE__")
def test_generate_website_no_movies(mock_file, mock_list_movies, mock_exists, capsys):
    movies.active_user = "TestUser"
    movies.generate_website()
    captured = capsys.readouterr()
    assert f"No movies available for {movies.active_user}" in captured.out
