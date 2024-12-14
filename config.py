import json
import os
import fnmatch

CONFIG_FILE = 'config.json'

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config if file doesn't exist
            default_config = {
                "blocked_items": {
                    "files": [
                        "users.json",
                        "config.json",
                        "requirements.txt",
                        "config.json",
                        "config_manager.py",
                        "filemanager.py",
                        "users.json",
                        "web.config",
                        "__pycache__",
                        "*.py",
                        "*.pyc"
                    ],
                    "folders": [
                        "__pycache__",
                        "instance",
                        "templates",
                        "custerr",
                        "Installer",
                        "logs",
                        "temp",
                        "cdn",
                        "public",
                        ".git"
                    ],
                    "patterns": [
                        ".*"
                    ],
                    "exceptions": {
                        "admin_can_see": True,
                        "allowed_files": [
                            ""
                        ],
                        "allowed_folders": [
                            "public",
                            "shared",
                            "downloads"
                        ]
                    }
                }
            }
            self.save_config(default_config)
            return default_config

    def save_config(self, config=None):
        if config is None:
            config = self.config
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

    def get_config(self):
        return self.config['blocked_items']

    def is_blocked(self, path, is_admin=False):
        """Check if a path is blocked based on configuration."""
        # If admin_can_see is true and user is admin, allow access
        if is_admin and self.config['blocked_items']['exceptions'].get('admin_can_see', True):
            return False

        path = os.path.normpath(path).lower()  # Convert to lowercase for case-insensitive comparison
        filename = os.path.basename(path).lower()
        
        # Check if path is in exceptions (allowed items)
        if self._is_allowed(path):
            return False

        # Check if the file or directory name matches any blocked folder name
        for folder in self.config['blocked_items']['folders']:
            folder = folder.lower()
            if folder in path.split(os.sep) or folder == filename:
                return True

        # Check if path matches any blocked patterns
        if any(fnmatch.fnmatch(filename, pattern.lower()) for pattern in self.config['blocked_items']['patterns']):
            return True

        # Check if path matches any blocked file patterns
        if any(fnmatch.fnmatch(filename, pattern.lower()) for pattern in self.config['blocked_items']['files']):
            return True

        return False

    def _is_allowed(self, path):
        """Check if a path is explicitly allowed."""
        path = os.path.normpath(path).lower()  # Convert to lowercase for case-insensitive comparison
        filename = os.path.basename(path).lower()

        # Check if file is explicitly allowed
        if any(allowed_file.lower() == filename for allowed_file in self.config['blocked_items']['exceptions']['allowed_files']):
            return True

        # Check if path contains any allowed folders
        for folder in self.config['blocked_items']['exceptions']['allowed_folders']:
            folder = folder.lower()
            if folder in path.split(os.sep):
                return True

        return False

    def add_blocked_file(self, filename):
        """Add a file to the blocked files list."""
        if filename not in self.config['blocked_items']['files']:
            self.config['blocked_items']['files'].append(filename)
            self.save_config()

    def add_blocked_folder(self, folder):
        """Add a folder to the blocked folders list."""
        if folder not in self.config['blocked_items']['folders']:
            self.config['blocked_items']['folders'].append(folder)
            self.save_config()

    def add_blocked_pattern(self, pattern):
        """Add a pattern to the blocked patterns list."""
        if pattern not in self.config['blocked_items']['patterns']:
            self.config['blocked_items']['patterns'].append(pattern)
            self.save_config()

    def add_allowed_file(self, filename):
        """Add a file to the allowed files list."""
        if filename not in self.config['blocked_items']['exceptions']['allowed_files']:
            self.config['blocked_items']['exceptions']['allowed_files'].append(filename)
            self.save_config()

    def add_allowed_folder(self, folder):
        """Add a folder to the allowed folders list."""
        if folder not in self.config['blocked_items']['exceptions']['allowed_folders']:
            self.config['blocked_items']['exceptions']['allowed_folders'].append(folder)
            self.save_config()

    def remove_blocked_file(self, filename):
        """Remove a file from the blocked files list."""
        if filename in self.config['blocked_items']['files']:
            self.config['blocked_items']['files'].remove(filename)
            self.save_config()

    def remove_blocked_folder(self, folder):
        """Remove a folder from the blocked folders list."""
        if folder in self.config['blocked_items']['folders']:
            self.config['blocked_items']['folders'].remove(folder)
            self.save_config()

    def remove_blocked_pattern(self, pattern):
        """Remove a pattern from the blocked patterns list."""
        if pattern in self.config['blocked_items']['patterns']:
            self.config['blocked_items']['patterns'].remove(pattern)
            self.save_config()

    def remove_allowed_file(self, filename):
        """Remove a file from the allowed files list."""
        if filename in self.config['blocked_items']['exceptions']['allowed_files']:
            self.config['blocked_items']['exceptions']['allowed_files'].remove(filename)
            self.save_config()

    def remove_allowed_folder(self, folder):
        """Remove a folder from the allowed folders list."""
        if folder in self.config['blocked_items']['exceptions']['allowed_folders']:
            self.config['blocked_items']['exceptions']['allowed_folders'].remove(folder)
            self.save_config()
