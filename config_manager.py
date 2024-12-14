import json
import fnmatch
import os

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "blocked_items": {
                    "files": [],
                    "folders": [],
                    "patterns": [],
                    "exceptions": {
                        "admin_can_see": True,
                        "allowed_files": [],
                        "allowed_folders": []
                    }
                }
            }

    def is_blocked(self, path, is_admin=False):
        if not path:
            return False

        # If admin can see blocked items and user is admin
        if is_admin and self.config["blocked_items"]["exceptions"]["admin_can_see"]:
            return False

        filename = os.path.basename(path)
        parent_folder = os.path.basename(os.path.dirname(path))
        
        # First check if it's in allowed folders or files
        if filename in self.config["blocked_items"]["exceptions"]["allowed_files"]:
            return False

        if os.path.isdir(path):
            if filename in self.config["blocked_items"]["exceptions"]["allowed_folders"]:
                return False
        else:
            # If it's a file, check if it's in an allowed folder
            if parent_folder in self.config["blocked_items"]["exceptions"]["allowed_folders"]:
                return False

        # Then check if it's in blocked items
        if filename in self.config["blocked_items"]["files"]:
            return True

        if os.path.isdir(path):
            if filename in self.config["blocked_items"]["folders"]:
                return True

        # Check pattern matches for files
        for pattern in self.config["blocked_items"]["files"]:
            if fnmatch.fnmatch(filename, pattern):
                return True

        # Check pattern matches for general patterns
        for pattern in self.config["blocked_items"]["patterns"]:
            if fnmatch.fnmatch(filename, pattern):
                # If it matches a pattern but is in allowed folders, still allow it
                if os.path.isdir(path) and filename in self.config["blocked_items"]["exceptions"]["allowed_folders"]:
                    return False
                if parent_folder in self.config["blocked_items"]["exceptions"]["allowed_folders"]:
                    return False
                return True

        return False

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def add_blocked_file(self, file_pattern):
        if file_pattern not in self.config["blocked_items"]["files"]:
            self.config["blocked_items"]["files"].append(file_pattern)
            self.save_config()

    def add_blocked_folder(self, folder_name):
        if folder_name not in self.config["blocked_items"]["folders"]:
            self.config["blocked_items"]["folders"].append(folder_name)
            self.save_config()

    def add_blocked_pattern(self, pattern):
        if pattern not in self.config["blocked_items"]["patterns"]:
            self.config["blocked_items"]["patterns"].append(pattern)
            self.save_config()

    def add_allowed_file(self, filename):
        if filename not in self.config["blocked_items"]["exceptions"]["allowed_files"]:
            self.config["blocked_items"]["exceptions"]["allowed_files"].append(filename)
            self.save_config()

    def add_allowed_folder(self, foldername):
        if foldername not in self.config["blocked_items"]["exceptions"]["allowed_folders"]:
            self.config["blocked_items"]["exceptions"]["allowed_folders"].append(foldername)
            self.save_config()

    def remove_blocked_file(self, file_pattern):
        if file_pattern in self.config["blocked_items"]["files"]:
            self.config["blocked_items"]["files"].remove(file_pattern)
            self.save_config()

    def remove_blocked_folder(self, folder_name):
        if folder_name in self.config["blocked_items"]["folders"]:
            self.config["blocked_items"]["folders"].remove(folder_name)
            self.save_config()

    def remove_blocked_pattern(self, pattern):
        if pattern in self.config["blocked_items"]["patterns"]:
            self.config["blocked_items"]["patterns"].remove(pattern)
            self.save_config()

    def remove_allowed_file(self, filename):
        if filename in self.config["blocked_items"]["exceptions"]["allowed_files"]:
            self.config["blocked_items"]["exceptions"]["allowed_files"].remove(filename)
            self.save_config()

    def remove_allowed_folder(self, foldername):
        if foldername in self.config["blocked_items"]["exceptions"]["allowed_folders"]:
            self.config["blocked_items"]["exceptions"]["allowed_folders"].remove(foldername)
            self.save_config()
