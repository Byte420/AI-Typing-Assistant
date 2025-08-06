#!/usr/bin/env python3
"""
Test script to verify ANSI support and display
"""

import os
import sys

def test_ansi_support():
    """Test ANSI support and display"""
    print("Testing ANSI Support...")
    print("=" * 40)
    
    # Test basic ANSI codes
    print("Testing basic colors:")
    print("\033[31mRed text\033[0m")
    print("\033[32mGreen text\033[0m")
    print("\033[34mBlue text\033[0m")
    print("\033[1mBold text\033[0m")
    
    print("\nTesting Unicode characters:")
    print("╭─ Test Box ─╮")
    print("│ Sample text │")
    print("╰─────────────╯")
    
    print("\nTesting emojis:")
    print("🧠 ⚡ 💬 🤖 📎 💰 📊 ℹ️ ❌")
    
    print("\nANSI Support Test Complete!")

if __name__ == "__main__":
    test_ansi_support() 