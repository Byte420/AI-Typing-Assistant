#!/usr/bin/env python3
"""
Setup script for AI Typing Assistant
"""

import os
import shutil

def setup_config():
    """Set up configuration file"""
    print("Setting up AI Typing Assistant...")
    print("=" * 50)
    
    # Check if config.py already exists
    if os.path.exists("config.py"):
        print("✓ config.py already exists")
        return
    
    # Copy template to config.py
    if os.path.exists("config_template.py"):
        shutil.copy("config_template.py", "config.py")
        print("✓ Created config.py from template")
        print("\n📝 Next steps:")
        print("1. Edit config.py and add your OpenAI API key")
        print("2. Get your API key from: https://platform.openai.com/api-keys")
        print("3. Run: python ai_typing_assistant.py")
    else:
        print("❌ config_template.py not found")
        print("Please create config.py manually with your API key")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    
    required_packages = ["openai", "keyboard", "pyperclip"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
    else:
        print("\n✓ All dependencies are installed")

def main():
    """Main setup function"""
    print("AI Typing Assistant - Setup")
    print("=" * 50)
    
    setup_config()
    check_dependencies()
    
    print("\n" + "=" * 50)
    print("Setup complete! 🎉")
    print("\nTo get started:")
    print("1. Add your OpenAI API key to config.py")
    print("2. Run: python ai_typing_assistant.py")
    print("3. Press Ctrl+G to activate the assistant")

if __name__ == "__main__":
    main() 