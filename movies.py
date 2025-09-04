import random
from omdb_api import fetch_movie
import movie_storage_sql as storage
import os

def list_movies():
    """List all movies from the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return
    for title, movie in movies.items():
        print(f"{title} ({movie['year']}), Rating: {movie['rating']:.1f}")

def add_movie():
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    movie_data = fetch_movie(title)
    if not movie_data:
        return  # Fehler wird schon in fetch_movie ausgegeben

    storage.add_movie(
        movie_data["title"],
        movie_data["year"],
        movie_data["rating"],
        movie_data["poster_url"]
    )
    print(f"Movie '{movie_data['title']}' added successfully!")

def delete_movie():
    """Delete a movie."""
    title = input("Which movie do you want to delete? ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    storage.delete_movie(title)

def update_movie_rating():
    """Update a movie's rating."""
    title = input("Which movie do you want to rate? ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    try:
        new_rating = float(input("New rating (1-10): "))
        if new_rating < 1 or new_rating > 10:
            print("Rating must be between 1 and 10.")
            return
    except ValueError:
        print("Rating must be a number between 1 and 10.")
        return

    storage.update_movie(title, new_rating)

def movies_sorted_by_rating():
    """Display movies sorted by rating."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return

    sorted_movies = sorted(
        movies.items(), key=lambda item: item[1]['rating'], reverse=True
    )
    print("Movies sorted by rating:")
    for title, movie in sorted_movies:
        print(f"{title} ({movie['year']}), Rating: {movie['rating']:.1f}")

def search_movies():
    """Search movies by title."""
    query = input("Search term for movie title: ").strip().lower()
    if not query:
        print("Search term cannot be empty.")
        return

    movies = storage.list_movies()
    found = False
    for title, movie in movies.items():
        if query in title.lower():
            print(f"{title} ({movie['year']}), Rating: {movie['rating']:.1f}")
            found = True
    if not found:
        print("No movies found.")

def movie_stats():
    """Display statistics: top and lowest rated movies."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return

    ratings = [movie["rating"] for movie in movies.values()]
    max_rating = max(ratings)
    min_rating = min(ratings)

    print("\nTop rated movies:")
    for title, movie in movies.items():
        if movie["rating"] == max_rating:
            print(f"{title} ({movie['year']}), Rating: {movie['rating']:.1f}")

    print("\nLowest rated movies:")
    for title, movie in movies.items():
        if movie["rating"] == min_rating:
            print(f"{title} ({movie['year']}), Rating: {movie['rating']:.1f}")

def generate_website():
    """Generate HTML website from movies in the database."""
    template_path = os.path.join("_static", "index_template.html")
    output_path = "index.html"

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Template file not found: {template_path}")
        return

    movies = storage.list_movies()
    if not movies:
        print("No movies available to generate the website.")
        return

    movie_grid = ""
    for title, data in movies.items():
        movie_grid += f"""
        <div class="movie-item">
            <img class="movie-poster" src="{data.get('poster_url', '')}" alt="{title}">
            <div class="movie-info">
                <h2 class="movie-title">{title}</h2>
                <p class="movie-year">{data['year']}</p>
                <p class="movie-rating">Rating: {data['rating']}</p>
            </div>
        </div>
        """

    html_content = template.replace("__TEMPLATE_TITLE__", "My Movie Library")
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Website was generated successfully.")

def random_movie():
    """Display a random movie from the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return

    title, movie = random.choice(list(movies.items()))
    print(f"Random movie: {title} ({movie['year']}), Rating: {movie['rating']:.1f}")

def main():
    """Main program loop."""
    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Generate website")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Bye!")
            break
        elif choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie_rating()
        elif choice == "5":
            movie_stats()
        elif choice == "6":
            random_movie()
        elif choice == "7":
            search_movies()
        elif choice == "8":
            movies_sorted_by_rating()
        elif choice == "9":
            generate_website()
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
