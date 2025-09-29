#!/usr/bin/env python
"""
Enhanced Path Detection Test
Tests edge cases for absolute vs relative path detection
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

def get_path_info(path):
    """Get detailed information about a path for debugging."""
    if not path:
        return "Empty path"
    
    info = []
    info.append(f"Path: '{path}'")
    info.append(f"os.path.isabs(): {os.path.isabs(path)}")
    info.append(f"is_absolute_path(): {is_absolute_path(path)}")
    
    if path.startswith('\\\\') or path.startswith('//'):
        info.append("Type: UNC path")
    elif len(path) >= 3 and path[1] == ':' and path[0].isalpha():
        info.append("Type: Windows drive path")
    elif path.startswith('/'):
        info.append("Type: Unix-style absolute path")
    else:
        info.append("Type: Relative path")
    
    return " | ".join(info)

def test_edge_cases():
    """Test various edge cases for path detection."""
    
    test_paths = [
        # Standard absolute paths
        "C:\\Projects\\MyProject\\output.exr",
        "D:\\render\\sequence.####.exr", 
        "/usr/local/nuke/output.exr",
        "//server/share/project/output.exr",
        "\\\\server\\share\\project\\output.exr",
        
        # Edge cases
        "",  # Empty string
        "   ",  # Whitespace only
        "relative/path/output.exr",  # Relative path
        "./relative/output.exr",  # Relative with ./
        "../relative/output.exr",  # Relative with ../
        "~/output.exr",  # Home directory (Unix)
        "%USERPROFILE%\\output.exr",  # Windows environment variable
        "$HOME/output.exr",  # Unix environment variable
        
        # Unusual but valid paths
        "c:\\",  # Root drive
        "C:",  # Drive letter only
        "/",  # Unix root
        "//",  # Double slash
        "\\\\",  # Double backslash
        "\\\\server",  # Incomplete UNC
        "//server",  # Incomplete UNC (forward)
        
        # Network drives
        "Z:\\project\\output.exr",
        "X:\\",
        
        # Mixed separators
        "C:\\project/subfolder\\output.exr",
        "//server\\share/project\\output.exr",
        
        # Special characters
        "C:\\project with spaces\\output.exr",
        "C:\\project-with-dashes\\output.exr",
        "C:\\project_with_underscores\\output.exr",
        "C:\\project (with parens)\\output.exr",
        
        # Long paths
        "C:\\" + "very_long_folder_name\\" * 10 + "output.exr",
        
        # Case variations
        "c:\\projects\\output.exr",  # Lowercase drive
        "C:/projects/output.exr",  # Forward slashes on Windows
    ]
    
    print("=" * 80)
    print("ENHANCED PATH DETECTION TEST")
    print("=" * 80)
    print(f"Operating System: {os.name}")
    print(f"Platform: {sys.platform}")
    print("=" * 80)
    
    for i, path in enumerate(test_paths, 1):
        print(f"\nTest {i:2d}: {get_path_info(path)}")
    
    print("\n" + "=" * 80)
    print("Test completed!")

if __name__ == "__main__":
    test_edge_cases()
