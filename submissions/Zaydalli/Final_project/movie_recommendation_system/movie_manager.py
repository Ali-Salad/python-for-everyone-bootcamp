import uuid
from datetime import datetime
from models import Movie
from utils import print_success, print_error, print_warning, Colors

class MovieManager:
    """Handles CRUD operations for movies, favorites, and watch history."""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.movies = self._load_movies()
        self.favorites = self._load_data("favorites")
        self.history = self._load_data("history")
        
    def _load_movies(self):
        data = self.data_manager.read_data("movies")
        return [Movie.from_dict(m) for m in data]
        
    def _save_movies(self):
        self.data_manager.write_data("movies", [m.to_dict() for m in self.movies])
        
    def _load_data(self, key):
        return self.data_manager.read_data(key)
        
    def _save_data(self, key, data):
        self.data_manager.write_data(key, data)

    def add_movie(self, title, category, year, description):
        """Adds a new movie to the system."""
        movie_id = str(uuid.uuid4())
        new_movie = Movie(movie_id, title, category, year, description)
        self.movies.append(new_movie)
        self._save_movies()
        print_success(f"Movie '{title}' added successfully!")
        
    def update_movie(self, movie_id, title=None, category=None, year=None, description=None):
        """Updates an existing movie."""
        movie = self.get_movie_by_id(movie_id)
        if movie:
            if title: movie.title = title
            if category: movie.category = category
            if year: movie.year = year
            if description: movie.description = description
            self._save_movies()
            print_success(f"Movie '{movie.title}' updated successfully!")
            return True
        print_error("Movie not found.")
        return False
        
    def delete_movie(self, movie_id):
        """Deletes a movie by ID."""
        movie = self.get_movie_by_id(movie_id)
        if movie:
            self.movies.remove(movie)
            self._save_movies()
            print_success("Movie deleted successfully!")
            return True
        print_error("Movie not found.")
        return False
        
    def get_movie_by_id(self, movie_id):
        for movie in self.movies:
            if movie.movie_id == movie_id:
                return movie
        return None
        
    def display_movies(self, movie_list=None):
        """Displays a list of movies."""
        movies_to_display = movie_list if movie_list is not None else self.movies
        if not movies_to_display:
            print_warning("No movies found.")
            return
            
        print(f"\n{Colors.UNDERLINE}{'ID':<38} | {'Title':<25} | {'Category':<15} | {'Year':<6} | {'Rating'}{Colors.ENDC}")
        for m in movies_to_display:
            print(f"{m.movie_id:<38} | {m.title[:25]:<25} | {m.category[:15]:<15} | {m.year:<6} | {m.average_rating:.1f}/5.0")
            
    def search_by_title(self, query):
        """Searches movies by title."""
        results = [m for m in self.movies if query.lower() in m.title.lower()]
        self.display_movies(results)
        
    def search_by_category(self, category):
        """Searches movies by category."""
        results = [m for m in self.movies if category.lower() in m.category.lower()]
        self.display_movies(results)
        
    # --- Favorites Management ---
    
    def add_favorite(self, user_id, movie_id):
        movie = self.get_movie_by_id(movie_id)
        if not movie:
            print_error("Movie not found.")
            return
            
        user_favorites = [f for f in self.favorites if f['user_id'] == user_id]
        if any(f['movie_id'] == movie_id for f in user_favorites):
            print_warning("Movie is already in your favorites.")
            return
            
        self.favorites.append({
            "user_id": user_id,
            "movie_id": movie_id
        })
        self._save_data("favorites", self.favorites)
        print_success(f"'{movie.title}' added to favorites!")
        
    def remove_favorite(self, user_id, movie_id):
        for fav in self.favorites:
            if fav['user_id'] == user_id and fav['movie_id'] == movie_id:
                self.favorites.remove(fav)
                self._save_data("favorites", self.favorites)
                print_success("Movie removed from favorites!")
                return
        print_error("Movie not found in favorites.")
        
    def view_favorites(self, user_id):
        user_fav_ids = [f['movie_id'] for f in self.favorites if f['user_id'] == user_id]
        fav_movies = [m for m in self.movies if m.movie_id in user_fav_ids]
        print(f"\n{Colors.OKCYAN}--- Your Favorite Movies ---{Colors.ENDC}")
        self.display_movies(fav_movies)
        
    # --- Watch History Management ---
    
    def add_to_history(self, user_id, movie_id):
        # Allow multiple watches, just append
        self.history.append({
            "user_id": user_id,
            "movie_id": movie_id,
            "date_watched": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self._save_data("history", self.history)
        
    def view_history(self, user_id):
        user_history = [h for h in self.history if h['user_id'] == user_id]
        if not user_history:
            print_warning("Your watch history is empty.")
            return
            
        # Sort by date descending
        user_history.sort(key=lambda x: x['date_watched'], reverse=True)
        
        print(f"\n{Colors.OKCYAN}--- Your Watch History ---{Colors.ENDC}")
        print(f"{Colors.UNDERLINE}{'Date Watched':<22} | {'Title'}{Colors.ENDC}")
        for entry in user_history:
            movie = self.get_movie_by_id(entry['movie_id'])
            title = movie.title if movie else "Unknown Movie"
            print(f"{entry['date_watched']:<22} | {title}")
