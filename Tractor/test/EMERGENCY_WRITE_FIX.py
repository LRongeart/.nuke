#!/usr/bin/env python
"""
Write Node Emergency Fix Script for Nuke

CRITICAL ISSUE: Write node error "You must specify a file name to write to"
This means Write nodes don't have proper output file paths configured.

IMMEDIATE SOLUTION:
1. Open your Nuke script that's failing to render
2. In Nuke, go to Window > Python Editor (or Script Editor)  
3. Copy and paste this entire script
4. Click "Run" or press Ctrl+Enter
5. Configure the Write node paths as prompted
6. Save your script
7. Re-submit to Tractor

This script will find all Write nodes and help you fix missing file paths.
"""

import nuke
import os

def fix_write_nodes_emergency():
    """
    Emergency fix for Write node file path errors
    Finds and helps configure Write node output paths
    """
    
    print("=" * 60)
    print("WRITE NODE EMERGENCY FIX")
    print("=" * 60)
    
    # Find all Write nodes
    write_nodes = []
    for node in nuke.allNodes():
        if node.Class() in ['Write', 'WriteGeo', 'WriteTank']:
            write_nodes.append(node)
    
    if not write_nodes:
        print("No Write nodes found in script.")
        return
    
    print(f"Found {len(write_nodes)} Write nodes to check:")
    
    issues_found = 0
    
    for write_node in write_nodes:
        print(f"\n--- Checking {write_node.name()} ---")
        
        try:
            # Check if file knob exists and has a value
            if 'file' in write_node.knobs():
                file_path = write_node['file'].value()
                
                if not file_path or file_path.strip() == "":
                    print(f"  ✗ ERROR: No file path specified")
                    issues_found += 1
                    
                    # Suggest a default path based on script location
                    script_path = nuke.scriptName()
                    if script_path:
                        script_dir = os.path.dirname(script_path)
                        script_name = os.path.splitext(os.path.basename(script_path))[0]
                        suggested_path = os.path.join(script_dir, "renders", f"{script_name}_{write_node.name()}.####.exr")
                        suggested_path = suggested_path.replace("\\", "/")
                        
                        print(f"  💡 SUGGESTED FIX:")
                        print(f"     Set file path to: {suggested_path}")
                        print(f"     Command: {write_node.name()}['file'].setValue('{suggested_path}')")
                        
                        # Auto-fix option
                        response = input(f"     Auto-fix {write_node.name()} with suggested path? (y/n): ")
                        if response.lower() == 'y':
                            # Create renders directory if it doesn't exist
                            renders_dir = os.path.join(script_dir, "renders")
                            if not os.path.exists(renders_dir):
                                os.makedirs(renders_dir)
                                print(f"     Created directory: {renders_dir}")
                            
                            write_node['file'].setValue(suggested_path)
                            print(f"     ✓ Fixed: {write_node.name()} file path set")
                            issues_found -= 1
                    else:
                        print(f"  💡 MANUAL FIX REQUIRED:")
                        print(f"     1. Select the {write_node.name()} node")
                        print(f"     2. In properties, set the 'file' field to a valid path")
                        print(f"     3. Example: C:/path/to/output/filename.####.exr")
                
                else:
                    print(f"  ✓ File path exists: {file_path}")
                    
                    # Check if path is relative
                    if not os.path.isabs(file_path):
                        print(f"  ⚠ WARNING: Relative path detected")
                        print(f"     Relative paths may fail on render farm")
                        
                        # Convert to absolute if script is saved
                        script_path = nuke.scriptName()
                        if script_path:
                            script_dir = os.path.dirname(script_path)
                            abs_path = os.path.abspath(os.path.join(script_dir, file_path))
                            abs_path = abs_path.replace("\\", "/")
                            
                            print(f"  💡 SUGGESTED FIX:")
                            print(f"     Convert to absolute path: {abs_path}")
                            
                            response = input(f"     Convert {write_node.name()} to absolute path? (y/n): ")
                            if response.lower() == 'y':
                                write_node['file'].setValue(abs_path)
                                print(f"     ✓ Converted to absolute path")
                    
                    # Check file format
                    file_ext = os.path.splitext(file_path)[1].lower()
                    if file_ext in ['.mov', '.mp4', '.avi']:
                        print(f"  ⚠ WARNING: Video format detected ({file_ext})")
                        print(f"     Video formats may cause issues on render farm")
                        print(f"     Consider using image sequence (.exr, .dpx, .tiff)")
                        
                        response = input(f"     Convert {write_node.name()} to EXR sequence? (y/n): ")
                        if response.lower() == 'y':
                            new_path = file_path.replace(file_ext, ".####.exr")
                            write_node['file'].setValue(new_path)
                            print(f"     ✓ Converted to EXR sequence: {new_path}")
            
            else:
                print(f"  ✗ ERROR: Write node has no 'file' knob")
                issues_found += 1
                
        except Exception as e:
            print(f"  ✗ ERROR checking {write_node.name()}: {e}")
            issues_found += 1
    
    print(f"\n" + "=" * 60)
    print(f"WRITE NODE FIX COMPLETE")
    if issues_found > 0:
        print(f"⚠ {issues_found} issues still need manual attention")
        print("Please fix the remaining issues before re-submitting to Tractor")
    else:
        print("✓ All Write nodes appear to be properly configured")
    print(f"=" * 60)
    print("\nNEXT STEPS:")
    print("1. Save your script (Ctrl+S)")
    print("2. Re-submit to Tractor")
    print("3. Monitor render logs for success")

# Run the emergency fix
if __name__ == "__main__":
    try:
        fix_write_nodes_emergency()
    except Exception as e:
        print(f"Write node fix failed: {e}")
        print("Please contact pipeline support for manual assistance.")
