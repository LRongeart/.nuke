#!/usr/bin/env python
"""
Direct Write Node Path Fix Script

This script directly fixes Write node paths in your Nuke script.
Run this in your original failing script to ensure Write2 has a proper file path.
"""

import nuke
import os

def fix_write_nodes_in_script():
    """Fix all Write nodes in the current script to have proper file paths"""
    
    print("=== DIRECT WRITE NODE PATH FIX ===")
    
    # Get script info
    script_path = nuke.scriptName()
    if script_path == "Root" or not script_path:
        print("ERROR: Script must be saved first")
        return False
    
    script_dir = os.path.dirname(script_path)
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    
    print(f"Script: {script_name}")
    print(f"Directory: {script_dir}")
    
    # Find all Write nodes
    write_nodes = []
    for node in nuke.allNodes():
        if node.Class() in ['Write', 'WriteGeo']:
            write_nodes.append(node)
    
    print(f"Found {len(write_nodes)} Write nodes")
    
    fixed_count = 0
    
    for write_node in write_nodes:
        node_name = write_node.name()
        current_path = write_node['file'].value()
        
        print(f"\nChecking {node_name}:")
        print(f"  Current path: '{current_path}'")
        
        if not current_path or current_path.strip() == "":
            # Generate a proper path
            output_filename = f"{script_name}_{node_name}.####.exr"
            renders_dir = os.path.join(script_dir, "renders")
            new_path = os.path.join(renders_dir, output_filename)
            new_path = new_path.replace("\\", "/")
            
            # Set the new path
            write_node['file'].setValue(new_path)
            print(f"  FIXED: Set to '{new_path}'")
            
            # Create renders directory
            try:
                if not os.path.exists(renders_dir):
                    os.makedirs(renders_dir)
                    print(f"  Created directory: {renders_dir}")
            except Exception as e:
                print(f"  Warning: Could not create directory: {e}")
            
            fixed_count += 1
            
        else:
            print(f"  OK: Already has path")
    
    if fixed_count > 0:
        # Save the script
        try:
            nuke.scriptSave()
            print(f"\nSUCCESS: Fixed {fixed_count} Write nodes and saved script")
            return True
        except Exception as e:
            print(f"ERROR: Could not save script: {e}")
            return False
    else:
        print("\nNo Write nodes needed fixing")
        return True

def verify_write_nodes():
    """Verify all Write nodes have valid paths"""
    
    print("\n=== VERIFICATION ===")
    
    all_good = True
    for node in nuke.allNodes():
        if node.Class() in ['Write', 'WriteGeo']:
            path = node['file'].value()
            if not path or path.strip() == "":
                print(f"ERROR: {node.name()} still has no file path")
                all_good = False
            else:
                print(f"OK: {node.name()} -> {path}")
    
    return all_good

def main():
    """Main function to fix and verify Write nodes"""
    
    success = fix_write_nodes_in_script()
    if success:
        verified = verify_write_nodes()
        if verified:
            print("\n🎉 SUCCESS: All Write nodes have valid file paths!")
            print("Your script is now ready for Tractor submission.")
            return True
        else:
            print("\n❌ Some Write nodes still need manual attention")
            return False
    else:
        print("\n❌ Failed to fix Write nodes")
        return False

if __name__ == "__main__":
    main()
