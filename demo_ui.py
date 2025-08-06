#!/usr/bin/env python3
"""
Demo script to showcase the new UI improvements
"""

# Import the UI functions from the main script
from ai_typing_assistant import (
    print_banner, print_separator, print_input_box, 
    print_response_box, print_info_box, print_error_box,
    print_cost_summary, BRIGHT_GREEN, BRIGHT_BLUE, BRIGHT_RED,
    ANSI_ENABLED
)

def demo_ui():
    """Demonstrate the new UI features"""
    print("AI Typing Assistant - UI Demo")
    print("=" * 50)
    print(f"ANSI Support: {'Enabled' if ANSI_ENABLED else 'Disabled (using fallback)'}")
    print("=" * 50)
    
    # Show startup banner
    print_banner()
    
    # Demo input box
    print("\n" + "=" * 50)
    print("Input Box Demo:")
    print_input_box("[>] Type your message")
    print("This is a sample user input")
    if ANSI_ENABLED:
        print(f"{BRIGHT_BLUE}╰{'─' * 20}╯{RESET}")
    else:
        print(f"╰{'─' * 20}╯")
    
    # Demo response box
    print("\n" + "=" * 50)
    print("Response Box Demo:")
    sample_response = """Here's a sample response from the AI assistant.

This demonstrates how the response is formatted with proper borders and spacing.

The text is clearly separated and easy to read."""
    print_response_box("[+] Response", sample_response, BRIGHT_GREEN if ANSI_ENABLED else "")
    
    # Demo info box
    print("\n" + "=" * 50)
    print("Info Box Demo:")
    print_info_box("[*] Status", "Processing completed successfully!", BRIGHT_BLUE if ANSI_ENABLED else "")
    
    # Demo cost summary
    print("\n" + "=" * 50)
    print("Cost Summary Demo:")
    print_cost_summary(0.001234, 2.45, "gpt-3.5-turbo")
    
    # Demo error box
    print("\n" + "=" * 50)
    print("Error Box Demo:")
    print_error_box("This is how errors are displayed with proper formatting.")
    
    # Demo separator
    print("\n" + "=" * 50)
    print("Separator Demo:")
    print_separator()
    
    print("\n" + "=" * 50)
    print("UI Demo completed!")

if __name__ == "__main__":
    # Define RESET for the demo
    RESET = "\033[0m" if ANSI_ENABLED else ""
    demo_ui() 