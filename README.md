# File Manager

A Python-based file management utility with a graphical user interface (GUI) for efficient file organization and manipulation.

![File Manager Screenshot](screenshot.png) <!-- You can add a screenshot of your application here -->

## Features

- **File Operations:**
  - Copy files and directories
  - Move files and directories
  - Delete files and directories
  - Rename files and folders
  - Create new directories

- **User Interface:**
  - Clean and intuitive GUI
  - Easy-to-navigate file browser
  - Drag-and-drop functionality
  - File preview capabilities

- **File Management:**
  - Sort files by name, date, size, or type
  - Search functionality
  - File filtering options
  - Bulk operations support

- **Additional Features:**
  - File path navigation
  - File properties viewer
  - Error handling and user feedback
  - Progress indicators for operations

## Prerequisites

- Python 3.x
- tkinter (usually comes with Python)
- Additional Python packages (if any, listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/laggis/File-Mananger.git
cd File-Mananger
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **Starting the Application:**
   - Launch the application using the command above
   - The main window will display your file system

2. **Basic Operations:**
   - **Copy:** Select file(s) and use the copy button or Ctrl+C
   - **Move:** Select file(s) and use the move button or Ctrl+X
   - **Delete:** Select file(s) and use the delete button or Del key
   - **Rename:** Select a file and use F2 or right-click menu

3. **Navigation:**
   - Use the address bar to enter specific paths
   - Double-click folders to navigate into them
   - Use the back/forward buttons for navigation history

4. **File Management:**
   - Sort files using column headers
   - Use the search bar to find specific files
   - Filter files by type using the filter dropdown

## Configuration

The application can be configured through the settings menu or by editing the config file:

```python
# Example configuration
SETTINGS = {
    'show_hidden_files': False,
    'default_view': 'details',
    'sort_by': 'name',
    'theme': 'light'
}
```

## Keyboard Shortcuts

- **Ctrl + C:** Copy selected files
- **Ctrl + X:** Cut selected files
- **Ctrl + V:** Paste files
- **Delete:** Delete selected files
- **F2:** Rename selected file
- **Ctrl + F:** Search files
- **Alt + ←:** Go back
- **Alt + →:** Go forward

## Error Handling

The application includes robust error handling for common scenarios:
- File access permissions
- Disk space limitations
- File in use conflicts
- Invalid file operations

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development

To set up the development environment:

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
python -m pytest tests/
```

## Troubleshooting

Common issues and solutions:

1. **GUI Not Launching:**
   - Verify tkinter installation
   - Check Python version compatibility
   - Confirm all dependencies are installed

2. **Permission Errors:**
   - Run the application with appropriate permissions
   - Check file/folder access rights
   - Verify user permissions

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/laggis/File-Mananger/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Future Features

- Cloud storage integration
- File compression support
- Advanced search capabilities
- Custom themes and layouts
- File preview enhancements

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created by Laggis

## Acknowledgments

- Thanks to all contributors
- Inspired by modern file management systems
- Built with Python and tkinter
