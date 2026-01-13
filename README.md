# PenguinHosting File Manager

A powerful, secure, and modern web-based file manager built with Flask. This application provides a sleek "Cyber/Glass" interface for managing files on your server with robust user authentication and role-based access control.

## 🚀 Features

- **📂 File Management**
  - Browse directories and view file details.
  - **Download as ZIP**: Select multiple files or folders (Ctrl+Click / Checkbox) and download them as a single ZIP archive.
  - Recursively zips folder contents.
  - Upload files and create new folders (Admin only).
  - Delete files and directories (Admin only).

- **🔐 Security & Access Control**
  - **Role-Based Access**: strict separation between **Admin** and **User** roles.
  - **Blocked Items**: Automatically protects sensitive system files (e.g., `*.py`, `config.json`, `__pycache__`) from being accessed or downloaded.
  - Configurable blocking rules via `config.json`.
  - Secure login and registration system.

- **🎨 Modern UI/UX**
  - Responsive design using **Tailwind CSS**.
  - Glass-morphism effect with a dark "Cyber" theme.
  - Context menus (Right-click) for quick actions.
  - Real-time loading indicators for large operations.

## 🛠️ Installation

1.  **Clone the repository** (or download the source code).

2.  **Install Dependencies**:
    Ensure you have Python 3.x installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Root Directory**:
    Open `filemanager.py` and set the `ROOT_DIR` variable to the folder you want to manage:
    ```python
    ROOT_DIR = r'D:\FileServer'  # Change this to your desired path
    ```
    *Note: If the path does not exist, it will default to the application's own directory.*

## 🚀 Usage

1.  **Start the Server**:
    ```bash
    python filemanager.py
    ```

2.  **Access the Interface**:
    Open your web browser and navigate to:
    `http://localhost:8001`

3.  **Default Admin Credentials**:
    On the first run, a default admin account is created:
    - **Username**: `admin`
    - **Password**: `admin`
    
    ⚠️ **IMPORTANT**: Log in and change this password immediately via the "Profile" page.

## ⚙️ Configuration

### `config.json`
This file controls which files and folders are hidden or blocked from users.
- **`files`**: List of filenames or patterns (e.g., `*.py`) to block.
- **`folders`**: List of directory names to hide (e.g., `temp`, `logs`).
- **`exceptions`**: Allow specific overrides (e.g., allowing admins to see blocked files).

### `users.json`
Stores user credentials (hashed) and role information. Created automatically on first run.

## 📝 Requirements

- Python 3.6+
- Flask
- Werkzeug
- humanize
- requests

## 🤝 Contributing

Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
