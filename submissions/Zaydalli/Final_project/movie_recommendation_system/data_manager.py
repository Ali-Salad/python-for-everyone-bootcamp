import json
import os

class DataManager:
    """Manages all JSON file read and write operations."""
    
    def __init__(self, data_dir="data"):
        # The data directory should be relative to this file's location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, data_dir)
        self.files = {
            "users": "users.json",
            "movies": "movies.json",
            "ratings": "ratings.json",
            "favorites": "favorites.json",
            "history": "history.json"
        }
        self._initialize_files()
        
    def _initialize_files(self):
        """Creates the data directory and JSON files if they do not exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        for key, filename in self.files.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    json.dump([], f)

    def _get_filepath(self, key):
        return os.path.join(self.data_dir, self.files[key])

    def read_data(self, key):
        """Reads data from the specified JSON file."""
        filepath = self._get_filepath(key)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def write_data(self, key, data):
        """Writes data to the specified JSON file."""
        filepath = self._get_filepath(key)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
