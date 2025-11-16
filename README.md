# Comment Remover

A utility for automatically removing comments from source code files in various programming languages.

## Features

- **Support for many languages**: Python, JavaScript, TypeScript, Java, C, C++, C#, CSS, HTML, XML, Lua, Ruby, PHP, Go, Rust, Swift, Kotlin, SQL, Shell, Batch, R, MATLAB, Scala, Dart
- **Smart removal**: 
  - Single-line comment removal
  - Multi-line comment removal
  - String literals preservation (comments inside strings are not removed)
- **Intelligent line processing**:
  - If a comment occupies the entire line - the entire line is removed
  - If a comment is after code - only the comment is removed
  - Automatic removal of extra spaces
- **Beautiful interface**: Progress bar with detailed information about the processing
- **Automatic language detection** by file extension

## Installation

### Requirements

- Python 3.7 or newer
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/comment_remover.git
cd comment_remover
```

2. Install dependencies:

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
pip install -r requirements.txt
```

## Usage

### Preparation

1. Place source code files in the `input/` folder
2. You can create subfolders inside `input/` - the structure will be preserved

### Running

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
python main.py
```

### Results

- Processed files (without comments) are saved to the `output/` folder
- The folder structure is fully preserved
- Original files in `input/` remain unchanged

## Examples

### Before processing (Python):
```python
# This is a comment
def hello():  # Greeting function
    """
    Multi-line comment
    """
    print("Hello")  # Output
```

### After processing:
```python
def hello():
    print("Hello")
```

### Before processing (JavaScript):
```javascript
// Single-line comment
function test() {  // Function
    /* Multi-line
       comment */
    console.log("Test");  // Log
}
```

### After processing:
```javascript
function test() {
    console.log("Test");
}
```

## Supported Languages

| Language | Extension | Single-line | Multi-line |
|----------|-----------|-------------|------------|
| Python | `.py` | `#` | `"""`, `'''` |
| JavaScript | `.js`, `.jsx` | `//` | `/* */` |
| TypeScript | `.ts`, `.tsx` | `//` | `/* */` |
| Java | `.java` | `//` | `/* */` |
| C/C++ | `.c`, `.cpp` | `//` | `/* */` |
| C# | `.cs` | `//` | `/* */` |
| CSS | `.css` | — | `/* */` |
| HTML | `.html` | — | `<!-- -->` |
| XML | `.xml` | — | `<!-- -->` |
| Lua | `.lua` | `--` | `--[[ ]]` |
| Ruby | `.rb` | `#` | `=begin`, `=end` |
| PHP | `.php` | `//`, `#` | `/* */` |
| Go | `.go` | `//` | `/* */` |
| Rust | `.rs` | `//` | `/* */` |
| Swift | `.swift` | `//` | `/* */` |
| Kotlin | `.kt` | `//` | `/* */` |
| SQL | `.sql` | `--` | `/* */` |
| Shell | `.sh` | `#` | — |
| Batch | `.bat` | `REM`, `::` | — |
| R | `.r` | `#` | — |
| MATLAB | `.m` | `%` | `%{ %}` |
| Scala | `.scala` | `//` | `/* */` |
| Dart | `.dart` | `//` | `/* */` |

## How It Works

### Code Safety

- The program does not remove comments located inside string literals
- Correct code structure is preserved
- Line breaks are processed correctly

### Space Handling

- Spaces and tabs before comments are removed
- Line breaks (`\n`) are preserved
- Empty lines created after comment removal are removed

## Project Structure

```
comment_remover/
├── input/              # Source files (created automatically)
├── output/             # Processed files (created automatically)
├── main.py             # Main script
├── requirements.txt    # Python dependencies
├── install.bat         # Dependencies installation script (Windows)
├── start.bat           # Program launch script (Windows)
├── LICENSE             # License
└── README.md           # Documentation
```

## License

MIT License. See [LICENSE](LICENSE) file for details.

## Author

This project was created to simplify working with source code and removing unnecessary comments before publication or code analysis.

## Support

If you found a bug or want to suggest an improvement:
- Create an Issue on GitHub
- Send a Pull Request

## Additional Information

### Limitations

- Files must be in UTF-8 encoding (or compatible)
- Very complex cases of nested comments may be processed incorrectly
- Regular expressions in code that look like comments are processed correctly thanks to string literal checking

### Performance

- Processing of large projects happens quickly
- Progress bar shows up-to-date information about the process
- Multithreading is not used, as I/O operations are not a bottleneck

---

**Enjoy!**
