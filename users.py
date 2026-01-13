from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime

USERS_FILE = 'users.json'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(USERS_FILE, 'w') as f:
            json.dump(self.users, f, indent=4)

    def init_users(self):
        if not self.users:
            # Create default admin user if no users exist
            self.users = {
                "admin": {
                    "password": generate_password_hash("admin"),
                    "is_admin": True
                }
            }
            self.save_users()
        return self.users

    def get_case_insensitive_username(self, username):
        """Helper function to find the actual username case in the users dict"""
        username_lower = username.lower()
        for existing_username in self.users:
            if existing_username.lower() == username_lower:
                return existing_username
        return None

    def verify_user(self, username, password):
        actual_username = self.get_case_insensitive_username(username)
        
        if not actual_username or actual_username not in self.users:
            return False, "User not found"
        
        if check_password_hash(self.users[actual_username]['password'], password):
            return True, actual_username
        return False, "Invalid password"

    def get_users(self):
        """Get list of all users with their details"""
        return [{"username": username, "is_admin": details["is_admin"]} 
                for username, details in self.users.items()]

    def create_user(self, username, password, is_admin=False):
        """Create a new user"""
        if self.get_case_insensitive_username(username):
            return False
        
        self.users[username] = {
            "password": generate_password_hash(password),
            "is_admin": is_admin
        }
        self.save_users()
        return True

    def remove_user(self, username):
        """Remove a user"""
        actual_username = self.get_case_insensitive_username(username)
        if actual_username and actual_username in self.users:
            del self.users[actual_username]
            self.save_users()
            return True
        return False

    def is_admin(self, username):
        """Check if a user is an admin"""
        actual_username = self.get_case_insensitive_username(username)
        if actual_username and actual_username in self.users:
            return self.users[actual_username].get('is_admin', False)
        return False

    def get_all_users(self):
        return {username: {'is_admin': data['is_admin']} for username, data in self.users.items()}

    def change_password(self, username, current_password, new_password):
        actual_username = self.get_case_insensitive_username(username)
        
        if not actual_username:
            return False, "User not found"
        
        if not check_password_hash(self.users[actual_username]['password'], current_password):
            return False, "Current password is incorrect"
        
        self.users[actual_username]['password'] = generate_password_hash(new_password)
        self.save_users()
        return True, "Password changed successfully"

    def get_user_details(self):
        return {username: {
            'is_admin': data['is_admin'],
            'created_at': data.get('created_at', 'N/A')
        } for username, data in self.users.items()}

    def get_user_data(self, username):
        """Get all data for a specific user."""
        if username.lower() in self.users:
            return self.users[username.lower()]
        return None

    def update_download_count(self, username):
        """Update download count for a user."""
        if username.lower() in self.users:
            current_time = datetime.now()
            user_data = self.users[username.lower()]
            
            # Initialize download tracking if not exists
            if 'downloads' not in user_data:
                user_data['downloads'] = {
                    'count': 0,
                    'last_reset': current_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Reset count if it's a new day
            last_reset = datetime.strptime(user_data['downloads']['last_reset'], '%Y-%m-%d %H:%M:%S')
            if current_time.date() > last_reset.date():
                user_data['downloads']['count'] = 0
                user_data['downloads']['last_reset'] = current_time.strftime('%Y-%m-%d %H:%M:%S')
            
            user_data['downloads']['count'] += 1
            self.save_users()
            return user_data['downloads']['count']
        return None

    def get_download_count(self, username):
        """Get current download count for a user."""
        if username.lower() in self.users:
            user_data = self.users[username.lower()]
            if 'downloads' in user_data:
                return user_data['downloads']['count']
        return 0

# Usage
user_manager = UserManager()
user_manager.init_users()
