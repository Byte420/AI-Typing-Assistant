#!/usr/bin/env python3
"""
Test script to demonstrate prompt wrapping functionality
"""

from ai_typing_assistant import wrap_output, print_input_box, ANSI_ENABLED, BRIGHT_BLUE, WRAP_WIDTH, WRAP_INDENT

def test_prompt_wrapping():
    """Test the prompt wrapping functionality"""
    print("Testing Prompt Wrapping Functionality:")
    print("=" * 50)
    print(f"Wrap width: {WRAP_WIDTH} characters")
    print(f"Indent: '{WRAP_INDENT}'")
    print("=" * 50)
    
    # Test cases for prompts
    test_prompts = [
        # Short prompt (no wrapping needed)
        "What is the capital of France?",
        
        # Long prompt that needs wrapping
        "I need help with a complex programming problem involving multiple threads and synchronization. Can you explain how to properly implement a thread-safe queue in Python with detailed examples?",
        
        # Very long prompt
        "I'm working on a machine learning project and I need to understand the differences between various algorithms like random forests, support vector machines, and neural networks. Can you provide a comprehensive comparison including their advantages, disadvantages, and use cases?",
        
        # Prompt with technical terms
        "How do I implement a RESTful API using Flask with proper authentication, database integration using SQLAlchemy, and deployment to AWS with Docker containers?",
        
        # Prompt with mathematical content
        "Can you explain the concept of gradient descent in machine learning, including the mathematical formulation and how it's used to optimize neural network parameters?",
        
        # Mixed content prompt
        "I need to create a web application that allows users to upload images, process them using computer vision algorithms, and store the results in a database. The app should also include user authentication and a responsive frontend."
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Original length: {len(prompt)} characters")
        print(f"Original prompt:\n{prompt}")
        
        # Simulate the prompt display process
        print_input_box("[>] Your prompt")
        
        # Apply word wrapping to the prompt
        wrapped_prompt = wrap_output(prompt, WRAP_WIDTH, WRAP_INDENT)
        print(f"{wrapped_prompt}")
        
        if ANSI_ENABLED:
            print(f"{BRIGHT_BLUE}╰{'─' * (len('[>] Your prompt') + 4)}╯")
        else:
            print(f"╰{'─' * (len('[>] Your prompt') + 4)}╯")
        
        # Show line-by-line analysis
        lines = wrapped_prompt.split('\n')
        print(f"\nLine analysis:")
        for j, line in enumerate(lines, 1):
            print(f"  Line {j}: {len(line)} chars - '{line}'")
    
    print("\n" + "=" * 50)
    print("Prompt wrapping test completed!")

if __name__ == "__main__":
    test_prompt_wrapping() 