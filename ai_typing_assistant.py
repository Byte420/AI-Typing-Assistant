#!/usr/bin/env python3

import os
import json
import pyperclip
import threading
import queue
import time
import signal
import sys
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# === WINDOWS ANSI SUPPORT ===
def enable_windows_ansi():
    """Enable ANSI support on Windows"""
    if os.name == 'nt':  # Windows
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except:
            return False
    return True

# Enable ANSI support
ANSI_ENABLED = enable_windows_ansi()

# === STYLING ===
# Define colors only if ANSI is supported, otherwise use empty strings
if ANSI_ENABLED:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Colors that work well in Windows Terminal
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLUE = "\033[44m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_RED = "\033[41m"
else:
    # Fallback: no colors
    RESET = BOLD = DIM = UNDERLINE = ""
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ""
    BRIGHT_RED = BRIGHT_GREEN = BRIGHT_YELLOW = BRIGHT_BLUE = BRIGHT_MAGENTA = BRIGHT_CYAN = BRIGHT_WHITE = ""
    BG_BLUE = BG_GREEN = BG_YELLOW = BG_RED = ""

# === CONFIGURATION ===
# Try to load configuration from config.py if it exists
try:
    from config import API_KEY, MAX_YEARLY_COST, DEFAULT_MODEL, WRAP_WIDTH, WRAP_INDENT
    HAS_API_KEY = API_KEY and API_KEY != "your-openai-api-key-here"
except ImportError:
    # Fallback configuration
    API_KEY = "your-openai-api-key-here"
    MAX_YEARLY_COST = 5.00
    DEFAULT_MODEL = "gpt-3.5-turbo"
    WRAP_WIDTH = 80
    WRAP_INDENT = "  "
    HAS_API_KEY = False

# Initialize OpenAI client if API key is available
client = None
if HAS_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY)
    except ImportError:
        HAS_API_KEY = False

# Local model responses for offline operation
LOCAL_RESPONSES = {
    "greeting": [
        "Hello! I'm your offline AI assistant. How can I help you today?",
        "Hi there! I'm here to assist you with your questions and tasks.",
        "Greetings! I'm your local AI assistant, ready to help."
    ],
    "general": [
        "That's an interesting question. Let me think about that for you.",
        "I understand what you're asking. Here's what I can tell you about that.",
        "That's a good point. Let me provide some insights on this topic.",
        "I see what you mean. Here's my perspective on that matter.",
        "That's a thoughtful question. Let me share some information about that."
    ],
    "technical": [
        "From a technical perspective, this involves several key considerations.",
        "Technically speaking, there are a few important aspects to consider here.",
        "In technical terms, this relates to several fundamental concepts.",
        "From a technical standpoint, this touches on several important principles."
    ],
    "creative": [
        "That's a creative idea! Let me explore some possibilities with you.",
        "I love the creativity in your question. Here are some interesting angles to consider.",
        "That's an imaginative approach. Let me suggest some creative solutions.",
        "Your creative thinking is inspiring. Here are some innovative perspectives."
    ],
    "helpful": [
        "I'd be happy to help you with that. Here's what I can suggest.",
        "Let me assist you with that. Here are some helpful approaches.",
        "I'm here to help! Here's what I can offer for your situation.",
        "I'd love to help you with this. Here are some useful suggestions."
    ],
    "thinking": [
        "Let me think about that for a moment...",
        "That's an interesting challenge. Let me consider the options...",
        "Hmm, that's a good question. Let me reflect on this...",
        "That's worth thinking about. Let me explore this further..."
    ]
}

# === GLOBAL STATE ===
prompt_queue = queue.Queue()
is_running = True
executor = ThreadPoolExecutor(max_workers=2)
selected_model = None  # Will be set during model selection

# === UI HELPER FUNCTIONS ===
def convert_latex_to_ascii(text):
    """Convert LaTeX math syntax to readable ASCII format"""
    import re
    
    # Convert LaTeX fractions: \frac{numerator}{denominator}
    text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1 / \2', text)
    
    # Convert LaTeX text blocks: \text{content}
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    
    # Convert LaTeX display math: \[ ... \]
    text = re.sub(r'\\\[(.*?)\\\]', r'\1', text, flags=re.DOTALL)
    
    # Convert LaTeX inline math: \( ... \)
    text = re.sub(r'\\\((.*?)\\\)', r'\1', text, flags=re.DOTALL)
    
    # Convert common LaTeX symbols to ASCII
    latex_to_ascii = {
        r'\approx': '≈',
        r'\leq': '≤',
        r'\geq': '≥',
        r'\neq': '≠',
        r'\pm': '±',
        r'\times': '×',
        r'\div': '÷',
        r'\sqrt': '√',
        r'\sum': 'Σ',
        r'\prod': 'Π',
        r'\int': '∫',
        r'\infty': '∞',
        r'\alpha': 'α',
        r'\beta': 'β',
        r'\gamma': 'γ',
        r'\delta': 'δ',
        r'\theta': 'θ',
        r'\lambda': 'λ',
        r'\mu': 'μ',
        r'\pi': 'π',
        r'\sigma': 'σ',
        r'\phi': 'φ',
        r'\omega': 'ω',
        r'\rightarrow': '→',
        r'\leftarrow': '←',
        r'\Rightarrow': '⇒',
        r'\Leftarrow': '⇐',
        r'\leftrightarrow': '↔',
        r'\Leftrightarrow': '⇔',
        r'\subset': '⊂',
        r'\supset': '⊃',
        r'\subseteq': '⊆',
        r'\supseteq': '⊇',
        r'\in': '∈',
        r'\notin': '∉',
        r'\cup': '∪',
        r'\cap': '∩',
        r'\emptyset': '∅',
        r'\forall': '∀',
        r'\exists': '∃',
        r'\nexists': '∄',
        r'\partial': '∂',
        r'\nabla': '∇',
        r'\cdot': '·',
        r'\circ': '∘',
        r'\bullet': '•',
        r'\diamond': '◇',
        r'\triangle': '△',
        r'\square': '□',
        r'\angle': '∠',
        r'\perp': '⊥',
        r'\parallel': '∥',
        r'\cong': '≅',
        r'\sim': '∼',
        r'\equiv': '≡',
        r'\propto': '∝',
        r'\oplus': '⊕',
        r'\otimes': '⊗',
        r'\ominus': '⊖',
        r'\oslash': '⊘',
        r'\bigoplus': '⨁',
        r'\bigotimes': '⨂',
        r'\bigcup': '⋃',
        r'\bigcap': '⋂',
        r'\sum_{': 'Σ_',
        r'\prod_{': 'Π_',
        r'\int_{': '∫_',
        r'\lim_{': 'lim_',
        r'\max_{': 'max_',
        r'\min_{': 'min_',
        r'\sup_{': 'sup_',
        r'\inf_{': 'inf_',
        r'\log_{': 'log_',
        r'\ln': 'ln',
        r'\exp': 'exp',
        r'\sin': 'sin',
        r'\cos': 'cos',
        r'\tan': 'tan',
        r'\csc': 'csc',
        r'\sec': 'sec',
        r'\cot': 'cot',
        r'\arcsin': 'arcsin',
        r'\arccos': 'arccos',
        r'\arctan': 'arctan',
        r'\sinh': 'sinh',
        r'\cosh': 'cosh',
        r'\tanh': 'tanh',
        r'\det': 'det',
        r'\dim': 'dim',
        r'\ker': 'ker',
        r'\im': 'im',
        r'\Re': 'Re',
        r'\Im': 'Im',
        r'\arg': 'arg',
        r'\deg': 'deg',
        r'\bmod': 'mod',
        r'\pmod': 'mod',
        r'\bmod{': 'mod(',
        r'\pmod{': 'mod(',
        r'\binom{': 'C(',
        r'\choose': 'C',
        r'\dbinom{': 'C(',
        r'\tbinom{': 'C(',
        r'\overline{': '¯',
        r'\underline{': '_',
        r'\widehat{': '^',
        r'\widetilde{': '~',
        r'\vec{': '→',
        r'\hat{': '^',
        r'\tilde': '~',
        r'\bar{': '¯',
        r'\dot{': '·',
        r'\ddot{': '··',
        r'\dddot{': '···',
        r'\ddddot{': '····',
        r'\prime': "'",
        r'\backslash': '\\',
        r'\{': '{',
        r'\}': '}',
        r'\$': '$',
        r'\#': '#',
        r'\&': '&',
        r'\%': '%',
        r'\~': '~',
        r'\^': '^',
        r'\\': '\\',
        r'\_': '_',
        r'\text{': '',
        r'\mathrm{': '',
        r'\mathbf{': '',
        r'\mathit{': '',
        r'\mathcal{': '',
        r'\mathbb{': '',
        r'\mathfrak{': '',
        r'\mathscr{': '',
        r'\mathsf{': '',
        r'\mathtt{': '',
        r'\textnormal{': '',
        r'\textrm{': '',
        r'\textsf{': '',
        r'\texttt{': '',
        r'\textup{': '',
        r'\textit{': '',
        r'\textsl{': '',
        r'\textsc{': '',
        r'\textmd{': '',
        r'\textlf{': '',
        r'\textbf{': '',
        r'\textsf{': '',
        r'\texttt{': '',
        r'\textup{': '',
        r'\textit{': '',
        r'\textsl{': '',
        r'\textsc{': '',
        r'\textmd{': '',
        r'\textlf{': '',
        r'\textbf{': '',
    }
    
    # Apply LaTeX to ASCII conversions
    for latex, ascii_char in latex_to_ascii.items():
        text = text.replace(latex, ascii_char)
    
    # Clean up any remaining LaTeX braces
    text = re.sub(r'\{([^}]*)\}', r'\1', text)
    
    # Clean up any remaining LaTeX commands
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def wrap_output(text, width=WRAP_WIDTH, indent=WRAP_INDENT):
    """Wrap text to specified width with proper indentation"""
    import textwrap
    
    # Split text into paragraphs (double newlines)
    paragraphs = text.split('\n\n')
    wrapped_paragraphs = []
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Wrap each paragraph
            wrapped = textwrap.fill(
                paragraph.strip(),
                width=width,
                initial_indent=indent,
                subsequent_indent=indent,
                break_long_words=False,
                break_on_hyphens=False
            )
            wrapped_paragraphs.append(wrapped)
        else:
            # Preserve empty paragraphs
            wrapped_paragraphs.append("")
    
    # Join paragraphs back together
    return '\n\n'.join(wrapped_paragraphs)

def print_banner():
    """Display startup banner"""
    if ANSI_ENABLED:
        banner = f"""
{BRIGHT_CYAN}.--------------------------------------------------.{RESET}
{BRIGHT_CYAN}|                                                  |{RESET}
{BRIGHT_CYAN}|   ____  _  _     _____    _____          _       |{RESET}
{BRIGHT_CYAN}|  |___ \\| || |   / ( _ )  /__   \\___  ___| |__    |{RESET}
{BRIGHT_CYAN}|    __) | || |_ / // _ \\    / /\\/ _ \\/ __| '_ \\   |{RESET}
{BRIGHT_CYAN}|   / __/|__   _/ /| (_) |  / / |  __/ (__| | | |  |{RESET}
{BRIGHT_CYAN}|  |_____|  |_|/_/  \\___/   \\/   \\___|\\___|_| |_|  |{RESET}
{BRIGHT_CYAN}|                                                  |{RESET}
{BRIGHT_CYAN}|                  248tech.com                     |{RESET}
{BRIGHT_CYAN}'--------------------------------------------------'{RESET}
{BRIGHT_CYAN}╭── AI Typing Assistant ──╮{RESET}
{BRIGHT_CYAN}│ Choose your AI model below │{RESET}
{BRIGHT_CYAN}╰──────────────────────────╯{RESET}
"""
    else:
        banner = f"""
.--------------------------------------------------.
|                                                  |
|   ____  _  _     _____    _____          _       |
|  |___ \\| || |   / ( _ )  /__   \\___  ___| |__    |
|    __) | || |_ / // _ \\    / /\\/ _ \\/ __| '_ \\   |
|   / __/|__   _/ /| (_) |  / / |  __/ (__| | | |  |
|  |_____|  |_|/_/  \\___/   \\/   \\___|\\___|_| |_|  |
|                                                  |
|                  248tech.com                     |
'--------------------------------------------------'
╭── AI Typing Assistant ──╮
│ Choose your AI model below │
╰──────────────────────────╯
"""
    print(banner)

def print_separator():
    """Print a clean separator line"""
    if ANSI_ENABLED:
        print(f"{DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    else:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def print_input_box(prompt_text):
    """Display an input box with clear instructions"""
    if ANSI_ENABLED:
        print(f"\n{BRIGHT_BLUE}╭─ {BRIGHT_WHITE}{prompt_text}{BRIGHT_BLUE} ─╮{RESET}")
        print(f"{BRIGHT_BLUE}│{RESET} ", end="", flush=True)
    else:
        print(f"\n╭─ {prompt_text} ─╮")
        print("│ ", end="", flush=True)

def print_response_box(title, content, color=BRIGHT_GREEN):
    """Display a response box with title and content"""
    if ANSI_ENABLED:
        print(f"\n{color}╭─ {BRIGHT_WHITE}{title}{color} ─╮{RESET}")
        
        # Split content into lines and format
        lines = content.split('\n')
        for line in lines:
            if line.strip():
                print(f"{color}│{RESET} {line}")
            else:
                print(f"{color}│{RESET}")
        
        print(f"{color}╰{'─' * (len(title) + 4)}╯{RESET}")
    else:
        print(f"\n╭─ {title} ─╮")
        
        # Split content into lines and format
        lines = content.split('\n')
        for line in lines:
            if line.strip():
                print(f"│ {line}")
            else:
                print("│")
        
        print(f"╰{'─' * (len(title) + 4)}╯")

def print_info_box(title, content, color=BRIGHT_BLUE):
    """Display an info box with title and content"""
    if ANSI_ENABLED:
        print(f"\n{color}╭─ {BRIGHT_WHITE}{title}{color} ─╮{RESET}")
        print(f"{color}│{RESET} {content}")
        print(f"{color}╰{'─' * (len(title) + 4)}╯{RESET}")
    else:
        print(f"\n╭─ {title} ─╮")
        print(f"│ {content}")
        print(f"╰{'─' * (len(title) + 4)}╯")

def print_error_box(content):
    """Display an error box"""
    if ANSI_ENABLED:
        print(f"\n{BRIGHT_RED}╭─ {BRIGHT_WHITE}Error{BRIGHT_RED} ─╮{RESET}")
        print(f"{BRIGHT_RED}│{RESET} {content}")
        print(f"{BRIGHT_RED}╰{'─' * 7}╯{RESET}")
    else:
        print(f"\n╭─ Error ─╮")
        print(f"│ {content}")
        print(f"╰{'─' * 7}╯")

def print_cost_summary(cost, total_cost, model):
    """Display cost summary for the selected model"""
    if model == "local-llm":
        summary = f"[*] {model.upper()} • OFFLINE • No cost • No internet required"
        print_info_box("Cost Summary", summary, BRIGHT_GREEN if ANSI_ENABLED else "")
    else:
        model_icon = "[*]" if model == "gpt-4o" else "[+]"
        percentage = (total_cost / MAX_YEARLY_COST) * 100
        
        # Color based on usage percentage
        if ANSI_ENABLED:
            if percentage > 80:
                cost_color = BRIGHT_RED
            elif percentage > 60:
                cost_color = BRIGHT_YELLOW
            else:
                cost_color = BRIGHT_GREEN
        else:
            cost_color = ""
        
        summary = f"{model_icon} {model.upper()} • ${cost:.6f} • ${total_cost:.2f} / ${MAX_YEARLY_COST:.2f} ({percentage:.1f}%)"
        print_info_box("Cost Summary", summary, cost_color)

# === SETUP ===
def ensure_dirs():
    """Safely create directories and files with error handling"""
    try:
        HOME_DIR = os.path.join(os.path.expanduser("~"), "Documents", "248Tech")
        LOG_DIR = os.path.join(HOME_DIR, "Logs")
        CHAT_LOG = os.path.join(LOG_DIR, "Chat", "chat_log.txt")
        USAGE_FILE = os.path.join(LOG_DIR, "usage.json")
        
        os.makedirs(os.path.dirname(CHAT_LOG), exist_ok=True)
        if not os.path.exists(CHAT_LOG):
            open(CHAT_LOG, "w", encoding="utf-8").close()
        if not os.path.exists(USAGE_FILE):
            with open(USAGE_FILE, "w") as f:
                json.dump({"input": 0, "output": 0, "total": 0.0}, f)
    except Exception as e:
        print_error_box(f"Error setting up directories: {e}")
        return False
    return True

def load_usage():
    """Safely load usage data with fallback"""
    try:
        HOME_DIR = os.path.join(os.path.expanduser("~"), "Documents", "248Tech")
        LOG_DIR = os.path.join(HOME_DIR, "Logs")
        USAGE_FILE = os.path.join(LOG_DIR, "usage.json")
        
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)
            # Validate data structure
            required_keys = ["input", "output", "total"]
            if all(key in data for key in required_keys):
                return data
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass
    return {"input": 0, "output": 0, "total": 0.0}

def save_usage(data):
    """Safely save usage data with error handling"""
    try:
        HOME_DIR = os.path.join(os.path.expanduser("~"), "Documents", "248Tech")
        LOG_DIR = os.path.join(HOME_DIR, "Logs")
        USAGE_FILE = os.path.join(LOG_DIR, "usage.json")
        
        with open(USAGE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print_error_box(f"Error saving usage: {e}")

def estimate_cost(model, input_t, output_t):
    """Calculate cost with validation"""
    PRICING = {
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        "gpt-4o": {"input": 2.50, "output": 10.00}
    }
    try:
        rate = PRICING[model]
        return round((input_t / 1_000_000) * rate["input"] + (output_t / 1_000_000) * rate["output"], 6)
    except KeyError:
        return 0.0

# === CHAT CONTEXT ===
def load_context():
    """Load recent chat context with size limits and error handling"""
    try:
        HOME_DIR = os.path.join(os.path.expanduser("~"), "Documents", "248Tech")
        LOG_DIR = os.path.join(HOME_DIR, "Logs")
        CHAT_LOG = os.path.join(LOG_DIR, "Chat", "chat_log.txt")
        
        if not os.path.exists(CHAT_LOG):
            return ""
        
        with open(CHAT_LOG, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Limit context size to prevent memory issues
        MAX_CONTEXT_SIZE = 10000
        if len(content) > MAX_CONTEXT_SIZE:
            content = content[-MAX_CONTEXT_SIZE:]
        
        lines = content.splitlines()
    except Exception as e:
        print_info_box("Warning", f"Could not load chat context: {e}", BRIGHT_YELLOW if ANSI_ENABLED else "")
        return ""
    
    exchanges = []
    current = []
    CONTEXT_EXCHANGES = 5
    
    # Process lines in reverse order for recent context
    for line in reversed(lines):
        if line.startswith("You:") or line.startswith("Assistant:"):
            current.insert(0, line)
            if len(current) == 2:
                exchanges.insert(0, "\n".join(current))
                current = []
        if len(exchanges) >= CONTEXT_EXCHANGES:
            break
    
    return "\n\n".join(exchanges)

def append_to_log(prompt, reply):
    """Safely append to chat log with error handling"""
    try:
        HOME_DIR = os.path.join(os.path.expanduser("~"), "Documents", "248Tech")
        LOG_DIR = os.path.join(HOME_DIR, "Logs")
        CHAT_LOG = os.path.join(LOG_DIR, "Chat", "chat_log.txt")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CHAT_LOG, "a", encoding="utf-8") as f:
            f.write(f"--- {timestamp} ---\n")
            f.write(f"You: {prompt}\n")
            f.write(f"Assistant: {reply}\n\n")
    except Exception as e:
        print_error_box(f"Error saving chat log: {e}")

# === LOCAL LLM FUNCTION ===
def generate_local_response(prompt):
    """Generate a response using local logic instead of API calls"""
    prompt_lower = prompt.lower()
    
    # Simple keyword-based response generation
    if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice(LOCAL_RESPONSES["greeting"])
    
    elif any(word in prompt_lower for word in ['help', 'assist', 'support']):
        return random.choice(LOCAL_RESPONSES["helpful"])
    
    elif any(word in prompt_lower for word in ['think', 'thought', 'consider', 'reflect']):
        return random.choice(LOCAL_RESPONSES["thinking"])
    
    elif any(word in prompt_lower for word in ['creative', 'imagine', 'design', 'art', 'story']):
        return random.choice(LOCAL_RESPONSES["creative"])
    
    elif any(word in prompt_lower for word in ['technical', 'code', 'programming', 'algorithm', 'system']):
        return random.choice(LOCAL_RESPONSES["technical"])
    
    else:
        # Generate a more contextual response based on prompt length and content
        if len(prompt) < 20:
            return random.choice(LOCAL_RESPONSES["general"])
        elif len(prompt) < 50:
            return random.choice(LOCAL_RESPONSES["helpful"])
        else:
            return random.choice(LOCAL_RESPONSES["general"]) + " " + random.choice(LOCAL_RESPONSES["thinking"])

def ask_local_llm(prompt, model, usage=None):
    """Send request to local LLM with simulated processing"""
    model_icon = "[*]"
    print_info_box(f"{model_icon} Local AI Assistant", f"Model: {model.upper()} • Processing your request...", BRIGHT_CYAN if ANSI_ENABLED else "")
    print_input_box("[>] Your prompt")
    
    # Apply word wrapping to the prompt
    wrapped_prompt = wrap_output(prompt, WRAP_WIDTH, WRAP_INDENT)
    print(f"{wrapped_prompt}")
    
    if ANSI_ENABLED:
        print(f"{BRIGHT_BLUE}╰{'─' * (len('[>] Your prompt') + 4)}╯{RESET}")
    else:
        print(f"╰{'─' * (len('[>] Your prompt') + 4)}╯")

    try:
        # Simulate processing time
        time.sleep(1.5)
        
        # Generate response using local logic
        reply = generate_local_response(prompt)
        
        # Convert LaTeX to ASCII before displaying
        clean_reply = convert_latex_to_ascii(reply)
        
        # Apply word wrapping to the response
        wrapped_reply = wrap_output(clean_reply, WRAP_WIDTH, WRAP_INDENT)
        
        # Save to log and copy to clipboard
        append_to_log(prompt, reply)  # Save original response to log
        
        # Display response
        print_response_box("[+] Response", wrapped_reply, BRIGHT_GREEN if ANSI_ENABLED else "")
        
        # Display cost summary (free for offline)
        print_cost_summary(0, 0, model)
        
        # Copy to clipboard
        pyperclip.copy(clean_reply)  # Copy cleaned response to clipboard
        print_info_box("[*] Status", "Copied to clipboard", BRIGHT_MAGENTA if ANSI_ENABLED else "")

    except Exception as e:
        print_error_box(f"Local LLM Error: {e}")

def ask_gpt(prompt, model, usage):
    """Send request to GPT with timeout and error handling"""
    model_icon = "[*]" if model == "gpt-4o" else "[+]"
    print_info_box(f"{model_icon} AI Assistant", f"Model: {model.upper()} • Processing your request...", BRIGHT_CYAN if ANSI_ENABLED else "")
    print_input_box("[>] Your prompt")
    
    # Apply word wrapping to the prompt
    wrapped_prompt = wrap_output(prompt, WRAP_WIDTH, WRAP_INDENT)
    print(f"{wrapped_prompt}")
    
    if ANSI_ENABLED:
        print(f"{BRIGHT_BLUE}╰{'─' * (len('[>] Your prompt') + 4)}╯{RESET}")
    else:
        print(f"╰{'─' * (len('[>] Your prompt') + 4)}╯")

    try:
        # Load context asynchronously
        context = load_context()
        full_prompt = f"{context}\nYou: {prompt}" if context else prompt

        # Make API call with timeout
        API_TIMEOUT = 30
        future = executor.submit(
            client.chat.completions.create,
            model=model,
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        response = future.result(timeout=API_TIMEOUT)
        reply = response.choices[0].message.content.strip()

        # Handle usage tracking
        usage_data = getattr(response, "usage", None)
        if usage_data:
            input_t = usage_data.prompt_tokens
            output_t = usage_data.completion_tokens
            cost = estimate_cost(model, input_t, output_t)

            usage["input"] += input_t
            usage["output"] += output_t
            usage["total"] += cost
            save_usage(usage)
        else:
            cost = 0

        # Convert LaTeX to ASCII before displaying
        clean_reply = convert_latex_to_ascii(reply)
        
        # Apply word wrapping to the response
        wrapped_reply = wrap_output(clean_reply, WRAP_WIDTH, WRAP_INDENT)
        
        # Save to log and copy to clipboard
        append_to_log(prompt, reply)  # Save original response to log
        
        # Display response
        print_response_box("[+] Response", wrapped_reply, BRIGHT_GREEN if ANSI_ENABLED else "")
        
        # Display cost summary
        print_cost_summary(cost, usage["total"], model)
        
        # Copy to clipboard
        pyperclip.copy(clean_reply)  # Copy cleaned response to clipboard
        print_info_box("[*] Status", "Copied to clipboard", BRIGHT_MAGENTA if ANSI_ENABLED else "")

    except TimeoutError:
        print_error_box(f"API request timed out after {API_TIMEOUT} seconds")
    except Exception as e:
        print_error_box(f"API Error: {e}")

# === MODEL SELECTION ===
def select_model():
    """Select the model to use for this session"""
    global selected_model
    
    print_separator()
    print_info_box("[*] Model Selection", "Choose your preferred AI model for this session", BRIGHT_CYAN if ANSI_ENABLED else "")
    
    # Show available options
    options = []
    if HAS_API_KEY:
        options.append("1. GPT-3.5 Turbo (Online)")
        options.append("2. GPT-4o (Online)")
    options.append("3. Local LLM (Offline)")
    
    print("\nAvailable models:")
    for option in options:
        print(f"  {option}")
    
    # Get user choice
    while True:
        choice = get_user_input("[*] Enter your choice (1-3)")
        if not choice:
            print_info_box("[i] Info", "Cancelled by user.", BRIGHT_YELLOW if ANSI_ENABLED else "")
            return False
        
        try:
            choice_num = int(choice)
            if choice_num == 1 and HAS_API_KEY:
                selected_model = "gpt-3.5-turbo"
                print_info_box("[i] Info", f"Selected model: {selected_model.upper()}", BRIGHT_GREEN if ANSI_ENABLED else "")
                return True
            elif choice_num == 2 and HAS_API_KEY:
                selected_model = "gpt-4o"
                print_info_box("[i] Info", f"Selected model: {selected_model.upper()}", BRIGHT_GREEN if ANSI_ENABLED else "")
                return True
            elif choice_num == 3:
                selected_model = "local-llm"
                print_info_box("[i] Info", f"Selected model: {selected_model.upper()} (OFFLINE)", BRIGHT_GREEN if ANSI_ENABLED else "")
                return True
            else:
                print_error_box("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print_error_box("Please enter a valid number (1, 2, or 3).")

def get_user_input(prompt_text, timeout=30):
    """Get user input with proper text input including spaces"""
    print_input_box(prompt_text)
    if ANSI_ENABLED:
        print(f"{BRIGHT_BLUE}│{RESET} (Press Enter to submit, Ctrl+C to cancel)")
        print(f"{BRIGHT_BLUE}│{RESET} ", end="", flush=True)
    else:
        print("│ (Press Enter to submit, Ctrl+C to cancel)")
        print("│ ", end="", flush=True)
    
    try:
        # Use standard input() for full text input with cursor
        user_input = input().strip()
        
        # Close the input box
        if ANSI_ENABLED:
            print(f"{BRIGHT_BLUE}╰{'─' * (len(prompt_text) + 4)}╯{RESET}")
        else:
            print(f"╰{'─' * (len(prompt_text) + 4)}╯")
        
        return user_input if user_input else None
        
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print()  # New line after Ctrl+C
        if ANSI_ENABLED:
            print(f"{BRIGHT_BLUE}╰{'─' * (len(prompt_text) + 4)}╯{RESET}")
        else:
            print(f"╰{'─' * (len(prompt_text) + 4)}╯")
        return None
    except EOFError:
        # Handle EOF gracefully
        print()  # New line after EOF
        if ANSI_ENABLED:
            print(f"{BRIGHT_BLUE}╰{'─' * (len(prompt_text) + 4)}╯{RESET}")
        else:
            print(f"╰{'─' * (len(prompt_text) + 4)}╯")
        return None

def prompt_flow():
    """Handle the prompt flow with continuous input loop"""
    global selected_model
    
    # Load usage data for online models
    usage = load_usage() if selected_model != "local-llm" else None
    
    # Check budget for online models
    if selected_model != "local-llm" and usage["total"] >= MAX_YEARLY_COST:
        print_error_box(f"Budget cap of ${MAX_YEARLY_COST:.2f} reached.")
        return

    try:
        print_separator()
        
        # Continuous input loop
        while is_running:
            # Get user prompt
            user_prompt = get_user_input("[>] Type your message")
            if not user_prompt:
                print_info_box("[i] Info", "Cancelled by user.", BRIGHT_YELLOW if ANSI_ENABLED else "")
                break
            
            # Process the request using the selected model
            if selected_model == "local-llm":
                ask_local_llm(user_prompt, selected_model)
            else:
                ask_gpt(user_prompt, selected_model, usage)
            
            # Show separator and prepare for next input
            print_separator()
            
    except KeyboardInterrupt:
        print_info_box("[i] Info", "Exiting prompt loop.", BRIGHT_YELLOW if ANSI_ENABLED else "")
    except Exception as e:
        print_error_box(f"Prompt Error: {e}")

# === SIGNAL HANDLING ===
def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global is_running
    if ANSI_ENABLED:
        print(f"\n{BRIGHT_GREEN}[*] Shutting down gracefully...{RESET}")
    else:
        print(f"\n[*] Shutting down gracefully...")
    is_running = False
    executor.shutdown(wait=False)
    sys.exit(0)

# === MAIN ===
if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize
    if not ensure_dirs():
        print_error_box("Failed to initialize. Exiting.")
        sys.exit(1)
    
    # Display startup banner
    print_banner()
    
    # Select model at startup
    if not select_model():
        print_error_box("Model selection cancelled. Exiting.")
        sys.exit(1)
    
    try:
        # Start the prompt flow directly
        prompt_flow()
    except KeyboardInterrupt:
        pass
    finally:
        is_running = False
        executor.shutdown(wait=True)
        if ANSI_ENABLED:
            print(f"\n{BRIGHT_GREEN}[*] Goodbye!{RESET}")
        else:
            print(f"\n[*] Goodbye!") 