import random
import re
from datetime import datetime
import os
import movie_storage_sql as storage  # nur einmal importieren
from omdb_api import fetch_movie


#  Helper Functions
active_user = None  # Global Active User

def get_user_movies():
    if not active_user:
        print("No active user selected.")
        return {}
    try:
        return storage.list_movies(active_user)
    except Exception as e:
        print(f"Error accessing movies for {active_user}: {e}")
        return {}


def get_numeric_input(prompt: str, min_val=None, max_val=None, float_allowed=False):
    """
    Prompts the user for a numeric input, validating it against optional min/max limits.
    Supports int or float input based on float_allowed.
    """
    value = None  # Initialisierung, um Warnungen zu vermeiden

    while True:
        user_input = input(prompt).strip()
        try:
            value = float(user_input) if float_allowed else int(user_input)
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        if min_val is not None and value < min_val:
            print(f"Value must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Value must be at most {max_val}.")
            continue

        return value


def choose_user():
    global active_user
    while True:
        users = storage.list_users()
        print("\nSelect a user:")
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user}")
        print(f"{len(users)+1}. Create new user")

        choice = get_numeric_input("Enter choice: ", 1, len(users)+1)
        if choice == len(users) + 1:
            new_user = input("Enter new username: ").strip()
            if new_user:
                try:
                    storage.add_user(new_user)
                    active_user = new_user
                    break
                except Exception as e:
                    print(f"Error creating user: {e}")
            else:
                print("Username cannot be empty.")
        else:
            active_user = users[choice - 1]
            break

    print(f"\nLogged in as: {active_user}\n")


#  Movie Functions

def list_movies():
    movies = get_user_movies()
    if not movies:
        print(f"No movies available for {active_user}.")
        return
    print(f"Movies for {active_user}:")
    for idx, (movie_id, movie) in enumerate(movies.items(), start=1):
        print(f"{idx}. {movie['title']} ({movie['year']}), Rating: {movie['rating']:.1f}")


def add_movie():
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    movie_data = fetch_movie(title)
    if not movie_data:
        print("Movie not found.")
        return

    try:
        storage.add_movie(
            movie_data["title"],
            movie_data["year"],
            movie_data["rating"],
            movie_data.get("poster_url", ""),
            user=active_user
        )
        print(f"Movie '{movie_data['title']}' added successfully for {active_user}!")
    except Exception as e:
        print(f"Error adding movie: {e}")


def select_movie():
    movies = get_user_movies()
    if not movies:
        return None, None
    print("Movies:")
    for idx, (movie_id, movie) in enumerate(movies.items(), start=1):
        print(f"{idx}. {movie['title']} ({movie['year']}), Rating: {movie['rating']:.1f}")
    choice = get_numeric_input("Enter number of movie: ", 1, len(movies))
    movie_id = list(movies.keys())[choice - 1]
    return movie_id, movies[movie_id]


def delete_movie():
    movie_id, movie = select_movie()
    if not movie_id:
        return
    try:
        storage.delete_movie(movie_id, user=active_user)
        print(f"Movie '{movie['title']}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting movie: {e}")


def update_movie_rating():
    movie_id, movie = select_movie()
    if not movie_id:
        return
    new_rating = get_numeric_input("New rating (1-10): ", 1, 10, float_allowed=True)
    try:
        storage.update_movie(movie_id, new_rating, user=active_user)
        print(f"Movie '{movie['title']}' rating updated to {new_rating}.")
    except Exception as e:
        print(f"Error updating rating: {e}")


def movies_sorted_by_rating():
    movies = get_user_movies()
    if not movies:
        return
    sorted_movies = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
    print(f"Movies sorted by rating for {active_user}:")
    for idx, (movie_id, movie) in enumerate(sorted_movies, start=1):
        print(f"{idx}. {movie['title']} ({movie['year']}), Rating: {movie['rating']:.1f}")


def search_movies():
    query = input("Search term for movie title: ").strip().lower()
    if not query:
        print("Search term cannot be empty.")
        return
    movies = get_user_movies()
    found = False
    print("Search results:")
    for idx, (movie_id, movie) in enumerate(movies.items(), start=1):
        if query in movie['title'].lower():
            print(f"{idx}. {movie['title']} ({movie['year']}), Rating: {movie['rating']:.1f}")
            found = True
    if not found:
        print("No movies found.")


def movie_stats():
    movies = get_user_movies()
    if not movies:
        return
    ratings = [movie["rating"] for movie in movies.values()]
    max_rating, min_rating = max(ratings), min(ratings)
    print("\nTop rated movies:")
    for idx, (movie_id, movie) in enumerate(movies.items(), start=1):
        if movie["rating"] == max_rating:
            print(f"{idx}. {movie['title']} ({movie['year']}), Rating: {movie['rating']:.1f}")
    print("\nLowest rated movies:")
    for idx, (movie_id, movie) in enumerate(movies.items(), start=1):
        if movie["rating"] == min_rating:
            print(f"{idx}. {movie['title']} ({movie['year']}), Rating: {movie['rating']:.1f}")


def random_movie():
    movies = get_user_movies()
    if not movies:
        return
    movie_id, movie = random.choice(list(movies.items()))
    print("Random movie:")
    print(f"{movie['title']} ({movie['year']}), Rating: {movie['rating']:.1f}")


def generate_website():
    if not active_user:
        print("No active user selected.")
        return

    template_path = os.path.join("templates", "index_template.html")
    output_dir = "generated_sites"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{active_user}.html")

    if not os.path.exists(template_path):
        print(f"Template file not found: {template_path}")
        return

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except Exception as e:
        print(f"Error reading template: {e}")
        return

    movies = storage.list_movies(active_user)
    if not movies:
        print(f"No movies available for {active_user} to generate website.")
        return

    #  Movie Grid
    movie_grid = ""
    for movie_id, data in movies.items():
        movie_grid += f"""
        <div class="movie-item">
            <img class="movie-poster" src="{data.get('poster_url', '')}" alt="{data['title']}">
            <div class="movie-info">
                <h2 class="movie-title">{data['title']}</h2>
                <p class="movie-year">{data['year']}</p>
                <p class="movie-rating">Rating: {data['rating']}</p>
            </div>
        </div>
        """


    # Dynamische Platzhalter ersetzen
    def replace_placeholder(match):
        key = match.group(0)
        if key == "__TEMPLATE_TITLE__":
            return f"{active_user}'s Movie Library"
        elif key == "__TEMPLATE_MOVIE_GRID__":
            return movie_grid
        elif key == "__TEMPLATE_DATE__":
            return datetime.now().strftime("%Y-%m-%d %H:%M")
        # Fallback: leerer String für unbekannte Platzhalter
        return ""

    html_content = re.sub(r"__\w+__", replace_placeholder, template)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Website for {active_user} was generated successfully: {output_path}")
    except Exception as e:
        print(f"Error writing website: {e}")


#  Main Program

def main():
    print("Welcome to the Movie App! 🎬")
    choose_user()

    menu = {
        "0": ("Exit", None),
        "1": ("List movies", list_movies),
        "2": ("Add movie", add_movie),
        "3": ("Delete movie", delete_movie),
        "4": ("Update movie", update_movie_rating),
        "5": ("Stats", movie_stats),
        "6": ("Random movie", random_movie),
        "7": ("Search movie", search_movies),
        "8": ("Movies sorted by rating", movies_sorted_by_rating),
        "9": ("Generate website", generate_website),
        "10": ("Switch user", choose_user)
    }

    while True:
        print("\nMenu:")
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")

        choice = input("Choose an option: ").strip()
        print()
        if choice in menu:
            if choice == "0":
                print("Bye!")
                break
            action = menu[choice][1]
            if action:
                action()
        else:
            print("Invalid input, please try again.")


#---------------- Start ---------------
if __name__ == "__main__":
    main()
