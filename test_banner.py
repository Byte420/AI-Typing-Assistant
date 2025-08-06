#!/usr/bin/env python3
"""
Test script to demonstrate the new 248tech.com banner
"""

from ai_typing_assistant import print_banner, ANSI_ENABLED

def test_new_banner():
    """Test the new 248tech.com banner"""
    print("Testing new 248tech.com banner:")
    print("=" * 50)
    
    # Show the new banner
    print_banner()
    
    print("\n" + "=" * 50)
    print(f"ANSI Support: {'Enabled' if ANSI_ENABLED else 'Disabled'}")
    print("Banner test completed!")

if __name__ == "__main__":
    test_new_banner() 