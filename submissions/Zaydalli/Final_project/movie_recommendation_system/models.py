class User:
    """Represents a user in the system."""
    
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        
    def to_dict(self):
        """Converts the User object to a dictionary for JSON serialization."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password
        }
        
    @classmethod
    def from_dict(cls, data):
        """Creates a User object from a dictionary."""
        return cls(
            user_id=data.get("user_id"),
            username=data.get("username"),
            password=data.get("password")
        )

class Movie:
    """Represents a movie in the system."""
    
    def __init__(self, movie_id, title, category, year, description, average_rating=0.0):
        self.movie_id = movie_id
        self.title = title
        self.category = category
        self.year = year
        self.description = description
        self.average_rating = average_rating
        
    def to_dict(self):
        """Converts the Movie object to a dictionary for JSON serialization."""
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "category": self.category,
            "year": self.year,
            "description": self.description,
            "average_rating": self.average_rating
        }
        
    @classmethod
    def from_dict(cls, data):
        """Creates a Movie object from a dictionary."""
        return cls(
            movie_id=data.get("movie_id"),
            title=data.get("title"),
            category=data.get("category"),
            year=data.get("year"),
            description=data.get("description"),
            average_rating=data.get("average_rating", 0.0)
        )
