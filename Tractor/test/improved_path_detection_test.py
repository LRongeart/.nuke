#!/usr/bin/env python
"""
Enhanced Path Detection Validation Test
Tests the improved dynamic expression detection logic
"""

import os
import sys

def is_absolute_path(path):
    """
    Enhanced path detection that handles various absolute path formats:
    - Windows: C:\path\to\file
    - UNC: \\server\share\path or //server/share/path  
    - Unix: /path/to/file
    - Network with drive: Z:\path\to\file
    """
    if not path or not isinstance(path, str):
        return False
    
    path = path.strip()
    if not path:
        return False
    
    # Use os.path.isabs as the primary check
    if os.path.isabs(path):
        return True
    
    # Additional checks for UNC paths that might not be caught
    # UNC paths: \\server\share or //server/share
    if path.startswith('\\\\') or path.startswith('//'):
        return True
    
    # Check for drive letters (Windows)
    if len(path) >= 3 and path[1] == ':' and path[0].isalpha():
        return True
    
    return False

def has_dynamic_expressions(path):
    """
    Check if path contains TCL expressions or environment variables 
    that should be resolved at render time rather than being converted.
    """
    if not path or not isinstance(path, str):
        return False
    
    # TCL expression indicators
    tcl_indicators = [
        '[',              # TCL expression brackets [file dirname ...]
        '${',             # Unix environment variables ${VAR}
        '$env(',          # TCL environment variables $env(VAR)
        '[getenv',        # TCL getenv function
        '[python',        # Python expressions in TCL
        '[value root',    # Common Nuke script references
        '[file ',         # TCL file operations
    ]
    
    # Windows environment variables %VAR%
    if '%' in path and path.count('%') >= 2:
        return True
    
    # Check for TCL indicators
    for indicator in tcl_indicators:
        if indicator in path:
            return True
    
    return False

def get_path_info(path):
    """Get detailed information about a path for debugging."""
    if not path:
        return "Empty path"
    
    info = []
    info.append(f"Path: '{path}'")
    info.append(f"os.path.isabs(): {os.path.isabs(path)}")
    info.append(f"is_absolute_path(): {is_absolute_path(path)}")
    info.append(f"has_dynamic_expressions(): {has_dynamic_expressions(path)}")
    
    if path.startswith('\\\\') or path.startswith('//'):
        info.append("Type: UNC path")
    elif len(path) >= 3 and path[1] == ':' and path[0].isalpha():
        info.append("Type: Windows drive path")
    elif path.startswith('/'):
        info.append("Type: Unix-style absolute path")
    elif has_dynamic_expressions(path):
        info.append("Type: Dynamic expression")
    else:
        info.append("Type: Relative path")
    
    return " | ".join(info)

def analyze_improved_path_scenario(path, description, expected_action):
    """Analyze a path scenario with the improved logic."""
    print(f"\n--- {description} ---")
    print(f"Expected: {expected_action}")
    
    # Determine action that would be taken with improved logic
    if not path or not path.strip():
        action = "AUTO-FIX: Generate default path"
    elif is_absolute_path(path):
        action = "ACCEPT: Absolute path detected"
    elif has_dynamic_expressions(path):
        action = "ACCEPT: Dynamic expression - let Nuke resolve"
    else:
        action = "WARN: Simple relative path (show warning but allow)"
    
    print(f"Actual:   {action}")
    print(get_path_info(path))
    
    # Check if improved logic matches expected behavior
    if expected_action in action or action in expected_action:
        status = "✅ CORRECT"
    else:
        status = "❌ NEEDS REVIEW"
    
    print(f"Status:   {status}")
    return status == "✅ CORRECT"

def test_improved_detection():
    """Test the improved dynamic expression detection."""
    
    print("=" * 80)
    print("IMPROVED PATH DETECTION VALIDATION")
    print("=" * 80)
    
    test_cases = [
        # Cases that should be accepted as dynamic expressions
        ("[file dirname [value root.name]]/renders/output.####.exr", "ACCEPT"),
        ("$PROJECT_ROOT/renders/output.####.exr", "ACCEPT"),
        ("${PROJECT_ROOT}/renders/output.####.exr", "ACCEPT"),
        ("[getenv PROJECT_ROOT]/renders/output.####.exr", "ACCEPT"),
        ("[python {nuke.script_directory()}]/renders/output.####.exr", "ACCEPT"),
        ("%USERPROFILE%/projects/output.exr", "ACCEPT"),
        ("%PROJECT_ROOT%/renders/output.####.exr", "ACCEPT"),
        ("$env(PROJECT_ROOT)/renders/output.####.exr", "ACCEPT"),
        ("[value root.name]/renders/output.####.exr", "ACCEPT"),
        ("[file tail [value root.name]].####.exr", "ACCEPT"),
        
        # Cases that should be accepted as absolute paths
        ("//tls-storage02/projects/MyProject/renders/output.####.exr", "ACCEPT"),
        ("C:/projects/MyProject/renders/output.####.exr", "ACCEPT"),
        ("Z:/shared/projects/output.####.exr", "ACCEPT"),
        ("\\\\tls-storage02\\Install\\NUKE\\projects\\output.####.exr", "ACCEPT"),
        
        # Cases that should show warning but allow (simple relative)
        ("renders/output.####.exr", "WARN"),
        ("../renders/output.####.exr", "WARN"),
        ("./renders/output.####.exr", "WARN"),
        ("output.exr", "WARN"),
        ("~/projects/output.exr", "WARN"),  # Unix home - not dynamic expression
        
        # Cases that should trigger auto-fix
        ("", "AUTO-FIX"),
        ("   ", "AUTO-FIX"),
        
        # Edge cases
        ("C:", "WARN"),  # Drive letter only - relative
        ("//server", "ACCEPT"),  # Incomplete UNC but still absolute
        ("$", "WARN"),  # Just dollar sign - not dynamic expression
        ("%", "WARN"),  # Just percent sign - not dynamic expression
        ("%INVALID", "WARN"),  # Incomplete environment variable
        ("$INVALID", "WARN"),  # Invalid Unix variable format
    ]
    
    correct_count = 0
    total_count = len(test_cases)
    
    for path, expected in test_cases:
        if analyze_improved_path_scenario(path, f"Path: '{path}'", expected):
            correct_count += 1
    
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Correct predictions: {correct_count}/{total_count}")
    print(f"Accuracy: {(correct_count/total_count)*100:.1f}%")
    
    if correct_count == total_count:
        print("🎉 All test cases passed! The improved logic works correctly.")
    else:
        print("⚠️  Some test cases need review. Check the logic above.")
    
    print("\n" + "=" * 80)
    print("BENEFITS OF IMPROVED DETECTION")
    print("=" * 80)
    print("✅ Windows environment variables (%VAR%) now properly detected")
    print("✅ TCL expressions properly identified and preserved")
    print("✅ Unix environment variables (${VAR}) properly handled")
    print("✅ Common Nuke script references detected")
    print("✅ Simple relative paths show warning but don't block submission")
    print("✅ Empty paths still trigger auto-fix as expected")

if __name__ == "__main__":
    test_improved_detection()
