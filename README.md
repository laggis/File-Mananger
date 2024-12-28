# FiveM Stream Splitter

A Python-based utility tool designed to split large FiveM stream files into smaller, more manageable chunks. This tool is particularly useful for managing large resource files that may cause streaming issues or exceed FiveM's file size limitations.

## Features

- **Automatic File Splitting:**
  - Splits large stream files into smaller chunks
  - Maintains file integrity during splitting
  - Configurable chunk sizes

- **Support for Multiple File Types:**
  - Handles common FiveM streaming files
  - Compatible with YTD files
  - Works with various resource formats

- **Easy to Use:**
  - Simple command-line interface
  - Minimal setup required
  - Automatic file organization

## Prerequisites

- Python 3.x
- Basic understanding of FiveM resource structure
- Windows/Linux compatible

## Installation

1. Clone the repository:
```bash
git clone https://github.com/laggis/Fivem-stream-spliter.git
cd Fivem-stream-spliter
```

2. Install Python if you haven't already:
   - Download from [Python.org](https://python.org)
   - Make sure to add Python to your PATH during installation

3. Install required dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

1. Place your large stream file(s) in the input directory

2. Run the script:
```bash
python stream_splitter.py
```

3. Follow the on-screen prompts:
   - Select input file
   - Choose desired chunk size
   - Confirm splitting operation

4. The split files will be created in the output directory

## Configuration

You can modify the default settings by adjusting the parameters in the script:
```python
# Example configuration
CHUNK_SIZE = 100000  # Adjust based on your needs
OUTPUT_DIR = "split_files"
```

## Best Practices

1. **Before Splitting:**
   - Back up your original files
   - Test with a small file first
   - Verify file permissions

2. **After Splitting:**
   - Test the split files in your FiveM server
   - Verify all chunks load correctly
   - Check resource performance

## Troubleshooting

Common issues and solutions:

1. **File Not Found Error:**
   - Verify file paths
   - Check file permissions
   - Ensure correct working directory

2. **Split Files Not Loading:**
   - Check file naming convention
   - Verify FiveM resource structure
   - Confirm file integrity

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/laggis/Fivem-stream-spliter/issues) page
2. Create a new issue with detailed information
3. Include any error messages and steps to reproduce

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created by Laggis

## Disclaimer

Always backup your files before using any splitting tools. While this tool is designed to maintain file integrity, it's always better to be safe than sorry!
