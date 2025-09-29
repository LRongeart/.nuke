#!/usr/bin/env python
"""
Targeted Write2 Node Fix Script

This script specifically fixes the Write2 node that's causing the 
"You must specify a file name to write to" error.

Run this in your original Nuke script that's failing to render.
"""

import nuke
import os

def fix_write2_node():
    """Fix the Write2 node specifically"""
    
    print("=== FIXING WRITE2 NODE ===")
    
    # Find Write2 node specifically
    write2_node = None
    try:
        write2_node = nuke.toNode('Write2')
    except:
        pass
    
    if write2_node is None:
        # Try finding any node named Write2
        for node in nuke.allNodes():
            if node.name() == 'Write2':
                write2_node = node
                break
    
    if write2_node is None:
        print("ERROR: Write2 node not found in script")
        return False
    
    print("Found Write2 node: " + write2_node.name())
    
    # Check current file path
    current_path = write2_node['file'].value()
    print("Current path: '" + str(current_path) + "'")
    
    if not current_path or current_path.strip() == "":
        print("ERROR: Write2 has no file path - fixing...")
        
        # Generate proper path based on script
        script_path = nuke.scriptName()
        if script_path:
            script_dir = os.path.dirname(script_path)
            script_name = os.path.splitext(os.path.basename(script_path))[0]
            
            # Create a proper render path
            render_filename = script_name + "_comp.####.exr"
            new_path = os.path.join(script_dir, "renders", render_filename)
            new_path = new_path.replace("\\", "/")
            
            # Set the path
            write2_node['file'].setValue(new_path)
            print("FIXED: Write2 path set to: " + new_path)
            
            # Create directory if needed
            render_dir = os.path.join(script_dir, "renders")
            try:
                if not os.path.exists(render_dir):
                    os.makedirs(render_dir)
                    print("Created render directory: " + render_dir)
            except Exception as e:
                print("Warning: Could not create directory: " + str(e))
            
            return True
        else:
            print("ERROR: Script is not saved - cannot auto-generate path")
            print("MANUAL ACTION: Please set Write2 file path manually")
            return False
    else:
        print("Write2 already has a path: " + current_path)
        
        # Ensure it's absolute path
        if not os.path.isabs(current_path):
            script_path = nuke.scriptName()
            if script_path:
                script_dir = os.path.dirname(script_path)
                abs_path = os.path.abspath(os.path.join(script_dir, current_path))
                abs_path = abs_path.replace("\\", "/")
                write2_node['file'].setValue(abs_path)
                print("CONVERTED: Made path absolute: " + abs_path)
        
        return True

def verify_write2_fix():
    """Verify that Write2 is properly configured"""
    
    print("\n=== VERIFYING WRITE2 ===")
    
    write2_node = nuke.toNode('Write2')
    if write2_node:
        file_path = write2_node['file'].value()
        if file_path and file_path.strip():
            print("SUCCESS: Write2 has valid file path")
            print("Path: " + file_path)
            
            # Check if directory exists
            dir_path = os.path.dirname(file_path)
            if os.path.exists(dir_path):
                print("SUCCESS: Output directory exists")
            else:
                print("WARNING: Output directory does not exist: " + dir_path)
                print("Tractor may fail if it cannot create the directory")
            
            return True
        else:
            print("ERROR: Write2 still has no file path")
            return False
    else:
        print("ERROR: Write2 node not found")
        return False

def main():
    """Main function to fix Write2 and verify"""
    
    print("Write2 Node Fix Script")
    print("=" * 40)
    
    # Fix Write2
    fix_success = fix_write2_node()
    
    # Verify fix
    verify_success = verify_write2_fix()
    
    print("\n" + "=" * 40)
    if fix_success and verify_success:
        print("SUCCESS: Write2 is ready for rendering!")
        print("\nNext steps:")
        print("1. Save your script (Ctrl+S)")
        print("2. Re-submit to Tractor")
        print("3. Monitor render for success")
    else:
        print("ERROR: Write2 fix failed")
        print("Manual action required:")
        print("1. Select Write2 node")
        print("2. Set 'file' field to a valid path")
        print("3. Example: //tls-storage02/path/to/output.####.exr")

if __name__ == "__main__":
    main()
