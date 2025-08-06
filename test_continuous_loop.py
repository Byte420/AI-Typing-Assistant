#!/usr/bin/env python3
"""
Test script to demonstrate the new continuous input loop behavior
"""

from ai_typing_assistant import (
    print_banner, print_separator, print_info_box, 
    get_user_input, ANSI_ENABLED, BRIGHT_CYAN, BRIGHT_GREEN, BRIGHT_YELLOW
)

def test_continuous_loop():
    """Test the new continuous input loop"""
    print("AI Typing Assistant - Continuous Loop Test")
    print("=" * 50)
    
    # Show banner
    print_banner()
    
    # Simulate model selection at startup
    print("\n" + "=" * 50)
    print("Model Selection at Startup:")
    print_separator()
    print_info_box("[*] Model Selection", "Choose your preferred AI model for this session", BRIGHT_CYAN if ANSI_ENABLED else "")
    
    model_choice = get_user_input("[*] Use GPT-4o? (y/n)")
    if model_choice is None:
        print_info_box("[i] Info", "Cancelled by user.", BRIGHT_YELLOW if ANSI_ENABLED else "")
        return
    
    selected_model = "GPT-4o" if model_choice.lower() == "y" else "GPT-3.5-turbo"
    print_info_box("[i] Info", f"Selected model: {selected_model}", BRIGHT_GREEN if ANSI_ENABLED else "")
    
    # Simulate continuous input loop
    print("\n" + "=" * 50)
    print("Continuous Input Loop (Press Ctrl+C to exit):")
    print_separator()
    
    message_count = 0
    try:
        while True:
            message_count += 1
            print(f"\n--- Message {message_count} ---")
            
            user_prompt = get_user_input("[>] Type your message")
            if not user_prompt:
                print_info_box("[i] Info", "Cancelled by user.", BRIGHT_YELLOW if ANSI_ENABLED else "")
                break
            
            print(f"Processing with {selected_model}...")
            print(f"Response: This is a simulated response to '{user_prompt}'")
            print_separator()
            
    except KeyboardInterrupt:
        print_info_box("[i] Info", "Exiting continuous loop.", BRIGHT_YELLOW if ANSI_ENABLED else "")
    
    print(f"\n" + "=" * 50)
    print(f"Session completed! Processed {message_count} messages with {selected_model}")

if __name__ == "__main__":
    test_continuous_loop() 