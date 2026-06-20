from utils import print_success, print_error, print_warning, Colors

class RatingManager:
    """Handles rating movies and calculating averages."""
    
    def __init__(self, data_manager, movie_manager):
        self.data_manager = data_manager
        self.movie_manager = movie_manager
        self.ratings = self._load_ratings()
        
    def _load_ratings(self):
        return self.data_manager.read_data("ratings")
        
    def _save_ratings(self):
        self.data_manager.write_data("ratings", self.ratings)
        
    def rate_movie(self, user_id, movie_id, score):
        """Allows a user to rate a movie from 1 to 5."""
        if score < 1 or score > 5:
            print_error("Invalid rating. Must be between 1 and 5.")
            return
            
        movie = self.movie_manager.get_movie_by_id(movie_id)
        if not movie:
            print_error("Movie not found.")
            return
            
        # Check if user already rated this movie
        existing_rating = next((r for r in self.ratings if r['user_id'] == user_id and r['movie_id'] == movie_id), None)
        
        if existing_rating:
            existing_rating['score'] = score
            print_success("Rating updated successfully!")
        else:
            self.ratings.append({
                "user_id": user_id,
                "movie_id": movie_id,
                "score": score
            })
            print_success("Movie rated successfully!")
            
        self._save_ratings()
        self._update_movie_average(movie_id)
        
    def _update_movie_average(self, movie_id):
        """Calculates and updates the average rating for a movie."""
        movie_ratings = [r['score'] for r in self.ratings if r['movie_id'] == movie_id]
        if not movie_ratings:
            return
            
        avg = sum(movie_ratings) / len(movie_ratings)
        self.movie_manager.update_movie(movie_id, description=None) # A bit hacky, let's just modify the object directly
        
        movie = self.movie_manager.get_movie_by_id(movie_id)
        if movie:
            movie.average_rating = avg
            self.movie_manager._save_movies()

class RecommendationEngine:
    """Handles generating personalized movie recommendations."""
    
    def __init__(self, data_manager, movie_manager, rating_manager):
        self.data_manager = data_manager
        self.movie_manager = movie_manager
        self.rating_manager = rating_manager
        
    def generate_recommendations(self, user_id):
        """Generates recommendations based on user's favorite categories and top rated movies."""
        movies = self.movie_manager.movies
        ratings = self.rating_manager.ratings
        history = self.movie_manager.history
        
        # 1. Identify watched/rated movies
        watched_movie_ids = set([h['movie_id'] for h in history if h['user_id'] == user_id])
        rated_movie_ids = set([r['movie_id'] for r in ratings if r['user_id'] == user_id])
        excluded_ids = watched_movie_ids.union(rated_movie_ids)
        
        # 2. Find user's favorite categories based on highly rated movies (>= 4 stars)
        user_highly_rated = [r for r in ratings if r['user_id'] == user_id and r['score'] >= 4]
        fav_categories = set()
        for r in user_highly_rated:
            movie = self.movie_manager.get_movie_by_id(r['movie_id'])
            if movie:
                fav_categories.add(movie.category)
                
        # 3. Filter candidates: not watched/rated
        candidates = [m for m in movies if m.movie_id not in excluded_ids]
        
        if not candidates:
            print_warning("No new movies to recommend at the moment.")
            return []
            
        # 4. Score candidates
        scored_candidates = []
        for m in candidates:
            score = 0
            if m.category in fav_categories:
                score += 5 # High weight for favorite category
            score += m.average_rating # Weight based on average rating
            scored_candidates.append((score, m))
            
        # 5. Sort by score descending and take top 5
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        recommended_movies = [m for score, m in scored_candidates[:5]]
        
        print(f"\n{Colors.OKCYAN}--- Recommended For You ---{Colors.ENDC}")
        if recommended_movies:
            self.movie_manager.display_movies(recommended_movies)
        else:
            print_warning("Could not find suitable recommendations.")
            
        return recommended_movies
