#!/usr/bin/env python
"""
Quick test for Unix environment variable detection
"""

def has_dynamic_expressions(path):
    """Check if path contains dynamic expressions."""
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
    
    # Unix environment variables starting with $ (but not just $)
    if path.startswith('$') and len(path) > 1 and path[1].isalpha():
        return True
    
    # Check for TCL indicators
    for indicator in tcl_indicators:
        if indicator in path:
            return True
    
    return False

# Test specific cases
test_paths = [
    "$PROJECT_ROOT/renders/output.####.exr",
    "${PROJECT_ROOT}/renders/output.####.exr", 
    "%PROJECT_ROOT%/renders/output.####.exr",
    "$",
    "$1",
    "$INVALID"
]

print("Unix Environment Variable Detection Test:")
print("=" * 50)
for path in test_paths:
    result = has_dynamic_expressions(path)
    print(f"'{path}' -> {result}")
