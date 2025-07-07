#!/usr/bin/env python
"""
Diagnostic script to check Write2 node configuration in the problematic Nuke script.
Run this in Nuke to see what's happening with the Write2 node.
"""

import nuke
import os
import sys

def check_write2_node():
    """Check the Write2 node configuration in the current script."""
    
    print("=" * 60)
    print("WRITE2 NODE DIAGNOSTIC")
    print("=" * 60)
    
    # Check if Write2 node exists
    write_node = nuke.toNode("Write2")
    if not write_node:
        print("ERROR: Write2 node not found in current script!")
        
        # List all Write nodes
        all_writes = nuke.allNodes("Write")
        print("Available Write nodes: %s" % [n.name() for n in all_writes])
        return False
    
    print("Write2 node found: %s" % write_node)
    print("Write2 node class: %s" % write_node.Class())
    
    # Check file path
    try:
        file_path = write_node['file'].value()
        print("File path: '%s'" % file_path)
        
        if not file_path or file_path.strip() == "":
            print("ERROR: Write2 node has NO file path set!")
        else:
            print("File path length: %d" % len(file_path))
            print("File path is absolute: %s" % os.path.isabs(file_path))
            
            # Check if path contains TCL expressions
            if '[' in file_path or '$' in file_path:
                print("File path contains TCL expressions")
                
                # Try to evaluate the expression
                try:
                    evaluated_path = nuke.filename(write_node)
                    print("Evaluated path: '%s'" % evaluated_path)
                except Exception as eval_e:
                    print("Could not evaluate path: %s" % eval_e)
        
    except Exception as e:
        print("ERROR getting file path: %s" % e)
    
    # Check other relevant knobs
    try:
        file_type = write_node['file_type'].value()
        print("File type: %s" % file_type)
    except:
        print("Could not get file type")
    
    try:
        if 'channels' in write_node.knobs():
            channels = write_node['channels'].value()
            print("Channels: %s" % channels)
    except:
        print("Could not get channels")
    
    # Check if disabled
    try:
        disabled = write_node['disable'].value()
        print("Disabled: %s" % disabled)
    except:
        print("Could not check disabled state")
    
    # Check frame range
    try:
        first = write_node['first'].value()
        last = write_node['last'].value()
        print("Frame range: %d-%d" % (first, last))
    except:
        print("Could not get frame range")
    
    print("=" * 60)
    return True

def check_script_info():
    """Check current script information."""
    print("SCRIPT INFO:")
    
    try:
        script_name = nuke.scriptName()
        print("Script name: %s" % script_name)
    except:
        print("Could not get script name")
    
    try:
        script_dir = os.path.dirname(nuke.scriptName())
        print("Script directory: %s" % script_dir)
    except:
        print("Could not get script directory")

# If script file is provided as argument, open it first
if len(sys.argv) > 1:
    script_path = sys.argv[1]
    print("Opening script: %s" % script_path)
    try:
        nuke.scriptOpen(script_path)
        print("Script opened successfully")
    except Exception as e:
        print("ERROR opening script: %s" % e)
        sys.exit(1)

# Run the diagnostics
check_script_info()
check_write2_node()
