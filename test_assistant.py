#!/usr/bin/env python3
"""
Test script for AI Typing Assistant functions
"""

import os
import json
from datetime import datetime

# Import the functions we want to test
from ai_typing_assistant import (
    ensure_dirs, load_usage, save_usage, 
    load_context, append_to_log, estimate_cost
)

def test_basic_functions():
    """Test the basic utility functions"""
    print("Testing basic functions...")
    
    # Test directory creation
    result = ensure_dirs()
    print(f"✓ Directory setup: {'PASS' if result else 'FAIL'}")
    
    # Test usage loading/saving
    test_usage = {"input": 1000, "output": 500, "total": 0.001}
    save_usage(test_usage)
    loaded_usage = load_usage()
    print(f"✓ Usage tracking: {'PASS' if loaded_usage['input'] == 1000 else 'FAIL'}")
    
    # Test cost estimation
    cost = estimate_cost("gpt-3.5-turbo", 1000, 500)
    print(f"✓ Cost estimation: {'PASS' if cost > 0 else 'FAIL'} (${cost:.6f})")
    
    # Test context loading (should work even with empty file)
    context = load_context()
    print(f"✓ Context loading: {'PASS' if context is not None else 'FAIL'}")
    
    # Test log appending
    try:
        append_to_log("Test prompt", "Test response")
        print("✓ Log appending: PASS")
    except Exception as e:
        print(f"✗ Log appending: FAIL - {e}")

def test_error_handling():
    """Test error handling with malformed data"""
    print("\nTesting error handling...")
    
    # Test with corrupted usage file
    backup_file = "test_usage_backup.json"
    if os.path.exists("usage.json"):
        os.rename("usage.json", backup_file)
    
    try:
        # Create corrupted file
        with open("usage.json", "w") as f:
            f.write("invalid json content")
        
        usage = load_usage()
        print(f"✓ Corrupted file handling: {'PASS' if usage['input'] == 0 else 'FAIL'}")
        
    finally:
        # Restore original file
        if os.path.exists(backup_file):
            os.rename(backup_file, "usage.json")

if __name__ == "__main__":
    print("AI Typing Assistant - Function Test")
    print("=" * 40)
    
    test_basic_functions()
    test_error_handling()
    
    print("\n" + "=" * 40)
    print("Test completed!") 