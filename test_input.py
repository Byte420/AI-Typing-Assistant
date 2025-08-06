#!/usr/bin/env python3
"""
Test script to demonstrate improved input functionality
"""

from ai_typing_assistant import get_user_input, print_banner, print_separator

def test_input_functionality():
    """Test the improved input functionality"""
    print("AI Typing Assistant - Input Test")
    print("=" * 50)
    
    # Show banner
    print_banner()
    
    # Test input with spaces
    print("\n" + "=" * 50)
    print("Testing Input with Spaces:")
    print("Try typing a sentence with spaces and special characters.")
    
    result = get_user_input("[>] Test your input")
    
    if result:
        print(f"\nSuccess! You entered: '{result}'")
        print(f"   Length: {len(result)} characters")
        print(f"   Contains spaces: {'Yes' if ' ' in result else 'No'}")
    else:
        print("\nInput was cancelled or empty")
    
    # Test model choice
    print("\n" + "=" * 50)
    print("Testing Model Choice:")
    
    model_choice = get_user_input("[*] Choose model (y/n)")
    
    if model_choice:
        model = "GPT-4o" if model_choice.lower() == "y" else "GPT-3.5-turbo"
        print(f"\nYou chose: {model}")
    else:
        print("\nModel choice was cancelled")
    
    print("\n" + "=" * 50)
    print("Input test completed!")

if __name__ == "__main__":
    test_input_functionality() 