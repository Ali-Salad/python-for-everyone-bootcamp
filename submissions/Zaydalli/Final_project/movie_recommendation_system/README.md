# Movie Recommendation System CLI

A complete, Object-Oriented Command Line Interface (CLI) application for recommending movies, tracking watch history, and managing movie collections. Built entirely with standard Python libraries.

## Folder Structure

```
movie_recommendation_system/
├── main.py                # Entry point and CLI menus
├── auth.py                # User authentication (Login/Registration)
├── data_manager.py        # JSON read/write handlers
├── models.py              # User and Movie OOP classes
├── movie_manager.py       # CRUD operations, History, Favorites
├── recommendation.py      # Rating system and Recommendation Engine
├── utils.py               # Helpers for colored UI and input validation
├── requirements.txt       # Project dependencies
├── README.md              # Documentation
└── data/                  # Auto-generated JSON files
    ├── users.json
    ├── movies.json
    ├── ratings.json
    ├── favorites.json
    └── history.json
```

## Features

- **Authentication System**: Secure registration and login. Passwords and usernames are validated.
- **Movie Management**: Admins can add, update, search, and delete movies.
- **Rating System**: Rate movies from 1 to 5 stars. Automatic calculation of average ratings.
- **Recommendation Engine**: Recommends top-rated unwatched movies based on user's favorite categories.
- **Watch History & Favorites**: Track movies watched and mark favorites.
- **JSON Storage**: All data is stored persistently in JSON format. Files are created automatically if they don't exist.

## How to Run

1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd path/to/movie_recommendation_system
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Development Requirements
- Python 3.x
- No external libraries required (`requirements.txt` is provided for completeness).
