#!/usr/bin/env python3
"""
Test script to demonstrate LaTeX to ASCII conversion
"""

from ai_typing_assistant import convert_latex_to_ascii, print_response_box, ANSI_ENABLED, BRIGHT_GREEN

def test_latex_conversion():
    """Test the LaTeX to ASCII conversion"""
    print("Testing LaTeX to ASCII conversion:")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        # Fractions
        r"\[ \frac{4514}{100} \approx 45 \text{ tables} \]",
        r"\frac{1}{2} + \frac{1}{3} = \frac{5}{6}",
        
        # Text blocks
        r"The result is \text{approximately} 45 units",
        r"Calculate \text{the sum} of all values",
        
        # Math symbols
        r"x \leq y \geq z \neq w",
        r"\alpha + \beta = \gamma",
        r"\sum_{i=1}^{n} x_i",
        r"\int_{0}^{\infty} e^{-x} dx",
        
        # Complex expressions
        r"\[ \frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} \]",
        r"\[ \text{The area is} \frac{1}{2} \times \text{base} \times \text{height} \]",
        
        # Mixed content
        r"Here's a calculation: \[ \frac{4514}{100} \approx 45 \text{ tables} \] which shows the result.",
        
        # Edge cases
        r"\\frac{1}{2}",  # Double backslash
        r"\text{simple text}",
        r"\[ x^2 + y^2 = z^2 \]",
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Original: {test_case}")
        
        converted = convert_latex_to_ascii(test_case)
        print(f"Converted: {converted}")
        
        # Show in response box format
        print_response_box("[+] LaTeX Conversion", converted, BRIGHT_GREEN if ANSI_ENABLED else "")
    
    print("\n" + "=" * 50)
    print("LaTeX conversion test completed!")

if __name__ == "__main__":
    test_latex_conversion() 