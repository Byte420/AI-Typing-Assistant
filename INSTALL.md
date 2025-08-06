# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API Key**
   - Get an OpenAI API key from https://platform.openai.com/api-keys
   - Replace the API_KEY in `ai_typing_assistant.py` with your key

3. **Run the Assistant**
   ```bash
   python ai_typing_assistant.py
   ```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'keyboard'**
   ```bash
   pip install keyboard
   ```

2. **ModuleNotFoundError: No module named 'openai'**
   ```bash
   pip install openai
   ```

3. **ModuleNotFoundError: No module named 'pyperclip'**
   ```bash
   pip install pyperclip
   ```

4. **Permission Error on Windows**
   - Run PowerShell as Administrator
   - Or use: `pip install --user -r requirements.txt`

### Windows-Specific Notes

- The `keyboard` module may require administrator privileges on Windows
- If hotkeys don't work, try running the script as Administrator
- Some antivirus software may flag the keyboard module - add an exception if needed

### First Run

- The script will create necessary directories and files automatically
- If you get permission errors, check that the script can write to the Documents folder
- The script creates a `Logs` folder in your Documents directory

## Usage

1. Start the script: `python ai_typing_assistant.py`
2. Press `Ctrl+G` to activate the assistant
3. Type your prompt and press Enter
4. Choose your model (y/n for GPT-4o)
5. Wait for the response (automatically copied to clipboard)
6. Press `ESC` to exit

## Configuration

You can modify these settings in `ai_typing_assistant.py`:

- `HOTKEY`: Change the activation hotkey (default: "ctrl+g")
- `MAX_YEARLY_COST`: Change the budget limit (default: $5.00)
- `API_TIMEOUT`: Change API timeout (default: 30 seconds)
- `CONTEXT_EXCHANGES`: Change conversation context (default: 5 exchanges) 