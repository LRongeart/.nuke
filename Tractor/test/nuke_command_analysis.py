#!/usr/bin/env python
"""
Nuke Command Line Options Analysis and Fix

The issue with "You must specify a file name to write to" when using -X Write2
suggests that we need to either:
1. Fix the Write2 node to have a proper file path, OR  
2. Change the command line approach

Let's implement a better solution.
"""

def analyze_nuke_command_options():
    """
    Analyze Nuke command line options for render farm:
    
    -x script.nk    : Load script in GUI mode
    -t script.nk    : Load script in terminal mode (no GUI) 
    -i              : Interactive mode
    -X node_name    : Execute specific Write node (requires valid file path)
    -F frame_range  : Set frame range
    """
    
    current_approach = """
    Current: nuke.exe -V 2 -x script.nk -F 1-1 -X Write2
    Problem: Write2 has no file path, so -X Write2 fails
    """
    
    solutions = {
        "Solution 1": "Fix Write2 file path, keep using -X Write2",
        "Solution 2": "Use -t instead of -x for better render farm compatibility", 
        "Solution 3": "Use different approach that doesn't require -X"
    }
    
    return current_approach, solutions

def create_improved_command_approach():
    """
    Create an improved command line approach for Nuke rendering
    """
    
    # Option 1: Terminal mode with specific Write node (requires fixed file path)
    option1 = '''
    cmd = [
        nuke_exe,
        "-V", "2",         # Verbose output
        "-t", script_path, # Terminal mode (no GUI)  
        "-F", f"{frame}-{frame}",
        "-X", write_name   # Execute specific Write node
    ]
    '''
    
    # Option 2: Terminal mode, render all Write nodes
    option2 = '''
    cmd = [
        nuke_exe,
        "-V", "2",         # Verbose output
        "-t", script_path, # Terminal mode (no GUI)
        "-F", f"{frame}-{frame}"
        # No -X, renders all enabled Write nodes
    ]
    '''
    
    # Option 3: Use Nuke script execution approach
    option3 = '''
    cmd = [
        nuke_exe,
        "-V", "2",         # Verbose output  
        "-t",              # Terminal mode
        "-exec", f"nuke.render('{write_name}', {frame}, {frame})",
        script_path
    ]
    '''
    
    return option1, option2, option3

def main():
    """
    Main analysis and recommendation
    """
    
    print("=== NUKE COMMAND LINE ANALYSIS ===")
    
    current, solutions = analyze_nuke_command_options()
    print("Current Situation:")
    print(current)
    
    print("\nAvailable Solutions:")
    for sol, desc in solutions.items():
        print(f"{sol}: {desc}")
    
    print("\n=== RECOMMENDATION ===")
    print("Best approach: Fix Write2 file path AND use -t for terminal mode")
    print("This gives us:")
    print("1. Proper file paths for all Write nodes")
    print("2. Terminal mode for better render farm compatibility")
    print("3. Specific Write node execution for precise control")

if __name__ == "__main__":
    main()
