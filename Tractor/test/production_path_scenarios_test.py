#!/usr/bin/env python
"""
Real-World Path Detection Test
Tests specific edge cases that might occur in production Nuke environments
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

def has_tcl_expressions(path):
    """Check if path contains TCL expressions that might resolve to absolute paths."""
    if not path:
        return False
    
    tcl_indicators = [
        '[',          # TCL expression brackets
        '$',          # Variables
        './/',        # Current directory with double slash
        '..//',       # Parent directory with double slash
        '/./',        # Unix current directory notation
        '/../',       # Unix parent directory notation
    ]
    
    return any(indicator in path for indicator in tcl_indicators)

def analyze_path_scenario(path, description):
    """Analyze a specific path scenario."""
    print(f"\n--- {description} ---")
    print(f"Path: '{path}'")
    print(f"os.path.isabs(): {os.path.isabs(path)}")
    print(f"is_absolute_path(): {is_absolute_path(path)}")
    print(f"has_tcl_expressions(): {has_tcl_expressions(path)}")
    
    # Determine action that would be taken
    if not path or not path.strip():
        action = "AUTO-FIX: Generate default path"
    elif is_absolute_path(path):
        action = "ACCEPT: Absolute path detected"
    elif has_tcl_expressions(path):
        action = "ACCEPT: TCL expressions detected - let Nuke resolve"
    else:
        action = "CONVERT: Convert relative to absolute"
    
    print(f"Action: {action}")
    return action

def test_production_scenarios():
    """Test scenarios that might occur in production."""
    
    print("=" * 80)
    print("PRODUCTION PATH SCENARIOS TEST")
    print("=" * 80)
    
    scenarios = [
        # Standard cases that should work
        ("//tls-storage02/projects/MyProject/renders/output.####.exr", "Standard UNC network path"),
        ("C:/projects/MyProject/renders/output.####.exr", "Standard Windows absolute path"),
        ("Z:/shared/projects/output.####.exr", "Mapped network drive"),
        
        # Problematic relative paths
        ("renders/output.####.exr", "Simple relative path"),
        ("../renders/output.####.exr", "Parent directory relative"),
        ("./renders/output.####.exr", "Current directory relative"),
        
        # TCL expression cases
        ("[file dirname [value root.name]]/renders/output.####.exr", "TCL expression using script location"),
        ("$PROJECT_ROOT/renders/output.####.exr", "Environment variable"),
        ("[getenv PROJECT_ROOT]/renders/output.####.exr", "TCL getenv function"),
        ("[python {nuke.script_directory()}]/renders/output.####.exr", "Python expression in TCL"),
        
        # Edge cases that might cause issues
        ("", "Empty path"),
        ("   ", "Whitespace only"),
        ("output.exr", "Just filename"),
        ("C:", "Drive letter only"),
        ("//server", "Incomplete UNC"),
        
        # Mixed separator edge cases
        ("//server\\share/project\\renders/output.####.exr", "Mixed UNC separators"),
        ("C:\\projects/renders\\output.####.exr", "Mixed Windows separators"),
        
        # Unusual but valid network paths
        ("\\\\tls-storage02\\Install\\NUKE\\projects\\output.####.exr", "Backslash UNC path"),
        ("//tls-storage02/Install/NUKE/projects/output.####.exr", "Forward slash UNC path"),
        
        # Environment variable edge cases
        ("%USERPROFILE%/projects/output.exr", "Windows environment variable"),
        ("${HOME}/projects/output.exr", "Unix environment variable"),
        ("~user/projects/output.exr", "User home directory"),
        
        # Sequence notation variations
        ("C:/renders/shot_001.%04d.exr", "printf style sequence"),
        ("C:/renders/shot_001.#.exr", "Single hash sequence"),
        ("C:/renders/shot_001.##.exr", "Double hash sequence"),
        ("C:/renders/shot_001.####.exr", "Quad hash sequence"),
        ("C:/renders/shot_001.######.exr", "Six hash sequence"),
    ]
    
    results = {"AUTO-FIX": 0, "ACCEPT": 0, "CONVERT": 0}
    
    for path, description in scenarios:
        action = analyze_path_scenario(path, description)
        for key in results:
            if key in action:
                results[key] += 1
                break
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total scenarios tested: {len(scenarios)}")
    for action, count in results.items():
        print(f"{action}: {count} scenarios")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print("1. TCL expressions should be allowed to pass through for Nuke resolution")
    print("2. Simple relative paths should be converted to absolute based on script location")
    print("3. Empty paths should trigger auto-fix with default naming")
    print("4. Mixed separators should be normalized for farm compatibility")
    print("5. Environment variables need special handling or warning to users")

if __name__ == "__main__":
    test_production_scenarios()
