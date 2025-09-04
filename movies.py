import movie_storage

def list_movies():
    movies = movie_storage.get_movies()
    if not movies:
        print("Keine Filme vorhanden.")
        return
    for title, movie in movies.items():
        print(f"{title} ({movie['year']}), Bewertung: {movie['rating']:.1f}")

def add_movie():
    title = input("Filmtitel: ")
    year = int(input("Erscheinungsjahr: "))
    rating = float(input("Bewertung (1-10): "))
    try:
        movie_storage.add_movie(title, year, rating)
        print(f"Film '{title}' wurde hinzugefügt.")
    except ValueError as e:
        print(e)

def delete_movie():
    title = input("Welchen Film möchtest du löschen? ")
    try:
        movie_storage.delete_movie(title)
        print(f"Film '{title}' wurde gelöscht.")
    except ValueError as e:
        print(e)

def update_movie_rating():
    title = input("Welchen Film möchtest du bewerten? ")
    try:
        new_rating = float(input("Neue Bewertung (1-10): "))
        movie_storage.update_movie(title, new_rating)
        print(f"Bewertung von '{title}' wurde aktualisiert.")
    except ValueError as e:
        print(e)

def movies_sorted_by_rating():
    movies = movie_storage.get_movies()
    sorted_movies = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
    print("Filme sortiert nach Bewertung:")
    for title, movie in sorted_movies:
        print(f"{title} ({movie['year']}), Bewertung: {movie['rating']:.1f}")

def search_movies():
    query = input("Suchbegriff für Filmtitel: ").lower()
    found = False
    for title, movie in movie_storage.get_movies().items():
        if query in title.lower():
            print(f"{title} ({movie['year']}), Bewertung: {movie['rating']:.1f}")
            found = True
    if not found:
        print("Keine Filme gefunden.")

def movie_stats():
    movies = movie_storage.get_movies()
    if not movies:
        print("Keine Filme vorhanden.")
        return

    ratings = [movie["rating"] for movie in movies.values()]
    max_rating = max(ratings)
    min_rating = min(ratings)

    print("\nTop bewertete Filme:")
    for title, movie in movies.items():
        if movie["rating"] == max_rating:
            print(f"{title} ({movie['year']}), Bewertung: {movie['rating']:.1f}")

    print("\nSchlecht bewertete Filme:")
    for title, movie in movies.items():
        if movie["rating"] == min_rating:
            print(f"{title} ({movie['year']}), Bewertung: {movie['rating']:.1f}")

def main():
    while True:
        print("\nMenü:")
        print("0. Beenden")
        print("1. Filme auflisten")
        print("2. Film hinzufügen")
        print("3. Film löschen")
        print("4. Bewertung aktualisieren")
        print("5. Filme nach Bewertung sortieren")
        print("6. Filme suchen")
        print("7. Statistik anzeigen")

        choice = input("Wähle eine Option: ")

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
            print("Ungültige Eingabe, bitte erneut versuchen.")

if __name__ == "__main__":
    main()