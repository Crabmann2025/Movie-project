import movie_storage_sql as storage


def list_movies():
    """List all movies from the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return
    for title, movie in movies.items():
        print(f"{title} ({movie['year']}), Rating: {movie['rating']:.1f}")


def add_movie():
    """Add a new movie with validated input."""
    title = input("Movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    try:
        year = int(input("Release year: "))
        if year < 1888 or year > 2100:
            print("Please enter a valid year between 1888 and 2100.")
            return
    except ValueError:
        print("Year must be a number.")
        return

    try:
        rating = float(input("Rating (1-10): "))
        if rating < 1 or rating > 10:
            print("Rating must be between 1 and 10.")
            return
    except ValueError:
        print("Rating must be a number between 1 and 10.")
        return

    storage.add_movie(title, year, rating)


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


def main():
    """Main program loop."""
    while True:
        print("\nMenu:")
        print("0. Quit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update rating")
        print("5. Movies sorted by rating")
        print("6. Search movies")
        print("7. Show statistics")

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
            movies_sorted_by_rating()
        elif choice == "6":
            search_movies()
        elif choice == "7":
            movie_stats()
        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    main()
