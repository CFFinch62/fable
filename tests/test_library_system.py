#!/usr/bin/env python3
"""
Test script for the FABLE library system.
Tests INCLUDE, SAVE-LIBRARY, and related words.
"""

from fable.interpreter.interpreter import ForthInterpreter

def test_library_words():
    """Test that library management words are registered."""
    print("=" * 60)
    print("Testing Library System")
    print("=" * 60)
    
    interp = ForthInterpreter()
    
    # Test 1: Check that library words exist
    print("\n1. Checking library words are registered...")
    library_words = ['INCLUDE', 'SAVE-LIBRARY', 'LOADED-LIBRARIES', 'LIBRARY-PATH']
    for word in library_words:
        if interp.dictionary.contains(word):
            print(f"   ✓ {word} registered")
        else:
            print(f"   ✗ {word} NOT FOUND")
    
    # Test 2: Check library paths
    print("\n2. Testing LIBRARY-PATH...")
    try:
        interp.evaluate('LIBRARY-PATH')
        print("   ✓ LIBRARY-PATH executed")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: Test LOADED-LIBRARIES (should be empty initially)
    print("\n3. Testing LOADED-LIBRARIES (should be empty)...")
    try:
        interp.evaluate('LOADED-LIBRARIES')
        print("   ✓ LOADED-LIBRARIES executed")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 4: Try to load a library
    print("\n4. Testing INCLUDE with math-extended.fth...")
    try:
        interp.evaluate('S" math-extended.fth" INCLUDE')
        print("   ✓ Library loaded successfully")

        # Check if a word from the library exists
        if interp.dictionary.contains('ABS'):
            print("   ✓ ABS word found (from library)")
        else:
            print("   ✗ ABS word not found")

    except Exception as e:
        print(f"   ✗ Error loading library: {e}")
    
    # Test 5: Test a word from the library
    print("\n5. Testing ABS word from library...")
    try:
        # Clear stack first
        interp.data_stack.clear()
        interp.evaluate('-5 ABS')
        result = interp.pop()
        if result == 5:
            print(f"   ✓ ABS works correctly: -5 ABS = {result}")
        else:
            print(f"   ✗ ABS returned wrong value: {result}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 6: Check loaded libraries
    print("\n6. Checking LOADED-LIBRARIES after loading...")
    try:
        interp.evaluate('LOADED-LIBRARIES')
        print("   ✓ LOADED-LIBRARIES executed")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 7: Test SAVE-LIBRARY
    print("\n7. Testing SAVE-LIBRARY...")
    try:
        # Define a custom word
        interp.evaluate(': DOUBLE 2 * ;')
        interp.evaluate(': TRIPLE 3 * ;')
        
        # Save to library
        interp.evaluate('S" test-lib.fth" SAVE-LIBRARY')
        print("   ✓ SAVE-LIBRARY executed")
        
        # Check if file was created
        from pathlib import Path
        lib_file = Path.home() / '.config' / 'fable' / 'libraries' / 'test-lib.fth'
        if lib_file.exists():
            print(f"   ✓ Library file created: {lib_file}")
            print(f"\n   Contents:")
            with open(lib_file, 'r') as f:
                for line in f:
                    print(f"      {line.rstrip()}")
        else:
            print(f"   ✗ Library file not found: {lib_file}")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Library System Test Complete")
    print("=" * 60)

if __name__ == '__main__':
    test_library_words()

