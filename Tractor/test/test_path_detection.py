#!/usr/bin/env python
"""
Test script to demonstrate enhanced path detection for various formats.
"""

import os

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

def normalize_path_for_farm(path):
    """
    Normalize a path for render farm compatibility.
    Converts to forward slashes and ensures proper UNC format.
    """
    if not path:
        return path
    
    # Normalize path separators
    normalized = path.replace('\\', '/')
    
    # Ensure UNC paths start with // (not \\)
    if normalized.startswith('\\\\'):
        normalized = '//' + normalized[2:]
    
    return normalized

def get_path_info(path):
    """
    Get detailed information about a path for debugging.
    """
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
    
    normalized = normalize_path_for_farm(path)
    if normalized != path:
        info.append(f"Normalized: '{normalized}'")
    
    return " | ".join(info)

def test_path_detection():
    """Test various path formats"""
    
    test_paths = [
        # Windows absolute paths
        r"C:\Program Files\Nuke\nuke.exe",
        "C:/Program Files/Nuke/nuke.exe",
        r"D:\Projects\MyProject\comp.nk",
        
        # UNC paths
        r"\\tls-storage02\Install\NUKE\comp.nk",
        "//tls-storage02/Install/NUKE/comp.nk",
        r"\\server\share\path\to\file.exr",
        "//server/share/path/to/file.exr",
        
        # Network drive paths
        r"Z:\Projects\Shot01\comp.nk",
        "Z:/Projects/Shot01/comp.nk",
        
        # Unix absolute paths
        "/usr/local/nuke/comp.nk",
        "/home/user/projects/comp.nk",
        
        # Relative paths
        "comp.nk",
        "./comp.nk",
        "../comp.nk",
        "renders/beauty.####.exr",
        r"renders\beauty.####.exr",
        
        # TCL expressions
        "[value root.name].####.exr",
        "${HOME}/projects/comp.nk",
        
        # Edge cases
        "",
        None,
        "   ",
        ".",
        "..",
    ]
    
    print("=" * 100)
    print("PATH DETECTION TEST")
    print("=" * 100)
    
    for path in test_paths:
        try:
            print(get_path_info(path))
            print("-" * 80)
        except Exception as e:
            print(f"ERROR testing path '{path}': {e}")
            print("-" * 80)

if __name__ == "__main__":
    test_path_detection()
