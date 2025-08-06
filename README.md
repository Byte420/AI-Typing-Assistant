# AI Typing Assistant - Performance Optimized

A lightweight AI assistant that uses hotkey (Ctrl+G) to open a prompt, sends text to OpenAI's API, and copies the response to the clipboard. Optimized for performance, reliability, and beautiful terminal UI with full Windows compatibility.

## ✨ Key Improvements Made

### 1. **🎨 Visual Enhancements**
- **Clean ASCII formatting**: Uses ASCII-safe characters for consistent display across all terminals
- **Windows ANSI support**: Automatic detection and fallback for Windows CMD and Terminal
- **Input boxes**: Clear visual input areas with proper borders and instructions
- **Response boxes**: Well-formatted AI responses with proper spacing and hierarchy
- **Color-coded information**: Different colors for different types of information (info, error, success)
- **ASCII-safe icons**: [>] for user input, [+] for responses, [*] for status, [i] for info

### 2. **🖥️ Windows Compatibility**
- **Automatic ANSI detection**: Detects if terminal supports ANSI colors
- **Graceful fallback**: Uses plain text if ANSI is not supported
- **No raw escape codes**: Eliminates broken `[94m`, `[97m` display issues
- **Clean output**: No debug codes, ping times, or milliseconds displayed
- **Cross-terminal support**: Works in Windows CMD, PowerShell, and Windows Terminal

### 3. **⌨️ Input System Improvements**
- **Full text input**: Spacebar and all characters work properly
- **Standard input()**: Uses Python's built-in input() for reliable text entry
- **No keyboard conflicts**: Removed problematic keyboard event handling
- **Visible cursor**: Clear input prompt with cursor indicator
- **Multi-word support**: Full sentences and natural language input
- **Line editing**: Standard terminal line editing (backspace, arrow keys, etc.)

### 4. **🚀 Performance Optimizations**
- **Non-blocking input**: Replaced blocking `input()` calls with keyboard event-based input
- **API timeout handling**: Added 30-second timeout for API calls to prevent hanging
- **Context size limits**: Limited chat context to 10,000 characters to prevent memory issues
- **ThreadPoolExecutor**: Used for concurrent API calls with proper resource management

### 5. **🛡️ Error Handling & Reliability**
- **Comprehensive error handling**: Added try-catch blocks for all file operations
- **Graceful degradation**: Script continues working even if files are corrupted
- **Signal handling**: Proper shutdown on Ctrl+C or system signals
- **File validation**: Validates JSON structure and handles malformed files

### 6. **🧵 Thread Safety**
- **Daemon threads**: All background threads are daemon to prevent hanging on exit
- **Thread-safe operations**: File operations are properly synchronized
- **Resource cleanup**: Proper shutdown of thread pools and resources

### 7. **👤 User Experience**
- **Non-blocking prompts**: User can cancel input with Ctrl+C
- **Timeout protection**: Input prompts timeout after 30 seconds
- **Better feedback**: More informative error messages and status updates
- **Graceful shutdown**: Clean exit with proper resource cleanup
- **Visual hierarchy**: Clear separation between different types of information

### 8. **📐 LaTeX Math Conversion**
- **Automatic conversion**: LaTeX math syntax converted to readable ASCII
- **Fraction handling**: `\frac{numerator}{denominator}` → `numerator / denominator`
- **Text blocks**: `\text{content}` → `content`
- **Math symbols**: `\approx`, `\leq`, `\geq`, `\neq` → `≈`, `≤`, `≥`, `≠`
- **Display math**: `\[ ... \]` → clean content
- **Greek letters**: `\alpha`, `\beta`, `\gamma` → `α`, `β`, `γ`
- **Clean output**: No raw LaTeX commands in terminal display
- **Monospace friendly**: All conversions work in terminal environments

### 9. **📝 Word Wrapping**
- **Automatic wrapping**: AI responses wrapped to configurable width (default: 80 chars)
- **Word boundary preservation**: Wraps at word boundaries, not mid-word
- **Paragraph preservation**: Maintains paragraph structure with double newlines
- **Indentation**: Configurable indentation for wrapped lines (default: 2 spaces)
- **Configurable width**: Easy to adjust `WRAP_WIDTH` variable
- **Clean formatting**: Preserves readability in terminal environments
- **Prompt wrapping**: User prompts also wrapped to prevent layout breaks

## 🎯 Features

- **Hotkey activation**: Press Ctrl+G to trigger the assistant
- **Session-based model selection**: Choose model once at startup, used for entire session
- **Continuous input loop**: Input prompt reappears after each response
- **LaTeX conversion**: Automatically converts LaTeX math syntax to readable ASCII
- **Word wrapping**: Automatically wraps AI responses to readable width
- **Cost tracking**: Monitors API usage and costs with visual indicators
- **Chat history**: Maintains conversation context
- **Clipboard integration**: Automatically copies responses
- **Budget management**: Stops when $5 yearly limit is reached
- **Beautiful UI**: Clean, modern terminal interface with proper formatting
- **Windows compatibility**: Works seamlessly across all Windows terminals
- **Full text input**: Spacebar and all characters work properly
- **Graceful exit**: Ctrl+C exits input loop, ESC exits program

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ai-typing-assistant
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Configure your API key:**
   - Edit `config.py` and add your OpenAI API key
   - Get your API key from: https://platform.openai.com/api-keys

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the assistant:**
   ```bash
   python ai_typing_assistant.py
   ```

6. **Use the assistant:**
   - Press `Ctrl+G` to activate
   - Type your prompts and get AI responses
   - Press `ESC` to exit

## 📁 File Structure

```
ai-typing-assistant/
├── ai_typing_assistant.py          # Main script
├── config_template.py               # Configuration template
├── setup.py                        # Setup script
├── requirements.txt                 # Dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
├── demo_ui.py                      # UI demonstration
├── test_*.py                       # Test scripts
└── Logs/                           # Generated logs (gitignored)
    ├── Chat/
    │   └── chat_log.txt
    └── usage.json
```

## 🎨 UI Features

### Visual Elements
- **Startup Banner**: Clean welcome screen with instructions
- **Input Boxes**: Clear visual areas for user input with borders
- **Response Boxes**: Well-formatted AI responses with proper spacing
- **Info Boxes**: Color-coded information displays
- **Error Boxes**: Clear error messages with red borders
- **Cost Summary**: Visual cost tracking with percentage indicators
- **Separators**: Clean dividing lines between sections

### Input System
- **Full text support**: Spacebar, punctuation, and all characters work
- **Standard terminal editing**: Backspace, arrow keys, copy/paste
- **Cancel support**: Ctrl+C to cancel input at any time
- **Clear prompts**: Visual input boxes with instructions

### ASCII-Safe Icons
- **[>]**: User input prompts
- **[+]**: AI responses
- **[*]**: System status and model selection
- **[i]**: Information messages

### Color Scheme (when ANSI supported)
- **Blue**: Input areas and general information
- **Green**: Success messages and AI responses
- **Red**: Errors and warnings
- **Yellow**: Warnings and info messages
- **Cyan**: Processing and status information
- **Magenta**: Clipboard operations

### Fallback Mode (when ANSI not supported)
- **Clean borders**: Uses Unicode box characters without colors
- **Readable text**: All information clearly displayed
- **Same functionality**: All features work identically

## 🏃‍♂️ Performance Benefits

- **No more freezing**: Eliminated blocking input calls
- **Faster startup**: Optimized file operations and error handling
- **Responsive UI**: Non-blocking keyboard input
- **Memory efficient**: Limited context size prevents memory bloat
- **Crash-resistant**: Comprehensive error handling prevents crashes
- **Visual clarity**: Clear separation of different information types
- **No broken formatting**: Eliminated raw ANSI code display issues
- **Full text input**: Spacebar and all characters work properly

## 🔧 Troubleshooting

- **If script doesn't start**: Check API key and internet connection
- **If hotkey doesn't work**: Ensure no other application is using Ctrl+G
- **If files are corrupted**: Delete `usage.json` and `chat_log.txt` to reset
- **If API calls timeout**: Check internet connection and API key validity
- **If colors don't display**: Script automatically falls back to plain text
- **If you see raw ANSI codes**: This issue has been fixed - no more `[94m` displays
- **If spacebar doesn't work**: This issue has been fixed - full text input now works

## 📦 Dependencies

- `openai` - OpenAI API client
- `keyboard` - Hotkey and input handling
- `pyperclip` - Clipboard operations
- Standard Python libraries (os, json, threading, etc.)

## 💰 Cost Management

The script tracks API usage and stops when the $5 yearly budget is reached. Costs are calculated based on:
- GPT-3.5-turbo: $0.50 per 1M input tokens, $1.50 per 1M output tokens
- GPT-4o: $2.50 per 1M input tokens, $10.00 per 1M output tokens

## 🎮 Demo & Testing

- **UI Demo**: `python demo_ui.py` - See UI features without API
- **Input Test**: `python test_input.py` - Test input functionality
- **ANSI Test**: `python test_ansi.py` - Test ANSI support

## 🔄 Migration from Original

The improved version maintains all functionality of the original script while adding:
- Beautiful visual formatting with Windows compatibility
- Automatic ANSI detection and fallback
- **Fixed input system**: Spacebar and full text input now work
- Better error handling
- Improved user experience
- Performance optimizations
- Thread safety improvements
- **Fixed ANSI display issues**: No more raw escape codes or debug output
- **Clean ASCII formatting**: No emojis, consistent borders, readable output 