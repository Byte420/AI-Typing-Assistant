#!/usr/bin/env python3
"""
Test script to demonstrate word wrapping functionality
"""

from ai_typing_assistant import wrap_output, print_response_box, ANSI_ENABLED, BRIGHT_GREEN, WRAP_WIDTH, WRAP_INDENT

def test_word_wrapping():
    """Test the word wrapping functionality"""
    print("Testing Word Wrapping Functionality:")
    print("=" * 50)
    print(f"Wrap width: {WRAP_WIDTH} characters")
    print(f"Indent: '{WRAP_INDENT}'")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        # Short text (no wrapping needed)
        "This is a short response that should not need wrapping.",
        
        # Long text that needs wrapping
        "This is a very long response that contains many words and should definitely need to be wrapped to fit within the specified width limit. It should break at word boundaries and not in the middle of words.",
        
        # Text with paragraphs
        """This is the first paragraph of a multi-paragraph response. It contains several sentences and should be wrapped appropriately.

This is the second paragraph. It should be treated separately from the first paragraph and wrapped independently. Each paragraph should maintain its own structure.

This is the third paragraph with some very long words like supercalifragilisticexpialidocious that might be longer than the wrap width."""
        
        # Text with LaTeX (should be converted first)
        "Here's a mathematical expression: 4514 / 100 ≈ 45 tables. This should be wrapped properly even with the mathematical symbols and fractions.",
        
        # Very long single word
        "This response contains a very long word: pneumonoultramicroscopicsilicovolcanoconiosispneumonoultramicroscopicsilicovolcanoconiosispneumonoultramicroscopicsilicovolcanoconiosis that exceeds the wrap width.",
        
        # Mixed content
        """Here's a comprehensive response with multiple elements:

1. Short sentences that don't need wrapping.
2. Longer sentences that definitely need to be wrapped to fit within the specified width limit.
3. Mathematical expressions like 4514 / 100 ≈ 45 tables.
4. Lists and structured content.

This should all be wrapped properly while maintaining readability."""
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Original length: {len(test_case)} characters")
        print(f"Original text:\n{test_case}")
        
        wrapped = wrap_output(test_case, WRAP_WIDTH, WRAP_INDENT)
        print(f"\nWrapped text ({len(wrapped)} characters):")
        print_response_box("[+] Wrapped Response", wrapped, BRIGHT_GREEN if ANSI_ENABLED else "")
        
        # Show line-by-line analysis
        lines = wrapped.split('\n')
        print(f"\nLine analysis:")
        for j, line in enumerate(lines, 1):
            print(f"  Line {j}: {len(line)} chars - '{line}'")
    
    print("\n" + "=" * 50)
    print("Word wrapping test completed!")

if __name__ == "__main__":
    test_word_wrapping() 