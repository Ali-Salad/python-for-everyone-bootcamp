import uuid
from models import User
from utils import print_success, print_error, print_warning, input_string

class AuthManager:
    """Handles user registration, login, and session management."""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.current_user = None
        self.users = self._load_users()
        
    def _load_users(self):
        """Loads users from the JSON file."""
        user_data = self.data_manager.read_data("users")
        return [User.from_dict(u) for u in user_data]
        
    def _save_users(self):
        """Saves current users to the JSON file."""
        self.data_manager.write_data("users", [u.to_dict() for u in self.users])
        
    def _is_username_taken(self, username):
        """Checks if a username already exists."""
        for user in self.users:
            if user.username.lower() == username.lower():
                return True
        return False
        
    def register(self):
        """Handles the user registration process."""
        print("\n--- Register New Account ---")
        username = input_string("Enter username: ")
        
        if self._is_username_taken(username):
            print_error("Username already exists. Please choose a different one.")
            return False
            
        password = input_string("Enter password: ")
        confirm_password = input_string("Confirm password: ")
        
        if password != confirm_password:
            print_error("Passwords do not match. Registration failed.")
            return False
            
        user_id = str(uuid.uuid4())
        new_user = User(user_id, username, password)
        self.users.append(new_user)
        self._save_users()
        
        print_success("Registration successful! You can now log in.")
        return True
        
    def login(self):
        """Handles the user login process."""
        print("\n--- User Login ---")
        username = input_string("Enter username: ")
        password = input_string("Enter password: ")
        
        for user in self.users:
            if user.username.lower() == username.lower() and user.password == password:
                self.current_user = user
                print_success(f"Welcome back, {user.username}!")
                return True
                
        print_error("Invalid username or password.")
        return False
        
    def logout(self):
        """Logs out the current user."""
        if self.current_user:
            print_success(f"Goodbye, {self.current_user.username}!")
            self.current_user = None
        else:
            print_warning("No user is currently logged in.")
            
    def is_logged_in(self):
        """Checks if a user is currently logged in."""
        return self.current_user is not None
