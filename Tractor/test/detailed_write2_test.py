#!/usr/bin/env python
import nuke
import sys
import os

try:
    # Open the Nuke script
    script_path = r"//tls-storage02/3D2/_NUKE/3D2_NUKE_010_CG/ESMA_10_3D3_RebuildEnvironment/RebuildEnvironment_COMP_v001.nk"
    print("Opening Nuke script: %s" % script_path)
    nuke.scriptOpen(script_path)
    
    # Find the Write node
    write_name = "Write2"
    write_node = nuke.toNode(write_name)
    
    if not write_node:
        print("ERROR: Write node '%s' not found in script" % write_name)
        sys.exit(1)
    
    print("Write node found: %s" % write_node)
    
    # Check Write node file path
    file_path = write_node['file'].value()
    print("Write node file path: %s" % file_path)
    
    if not file_path or file_path.strip() == "":
        print("ERROR: Write node '%s' has no output file path" % write_name)
        sys.exit(1)
    
    # Set current frame and get evaluated filename
    frame = 1
    nuke.frame(frame)
    print("Current frame set to: %d" % nuke.frame())
    
    # Try different ways to get the output filename
    try:
        # Method 1: Using nuke.filename()
        evaluated_path1 = nuke.filename(write_node)
        print("nuke.filename() result: %s" % evaluated_path1)
    except Exception as e:
        print("nuke.filename() failed: %s" % e)
        evaluated_path1 = None
    
    try:
        # Method 2: Using file knob evaluation
        file_knob = write_node['file']
        evaluated_path2 = file_knob.evaluate()
        print("file.evaluate() result: %s" % evaluated_path2)
    except Exception as e:
        print("file.evaluate() failed: %s" % e)
        evaluated_path2 = None
    
    try:
        # Method 3: Manual frame substitution
        import re
        if '%04d' in file_path:
            evaluated_path3 = file_path.replace('%04d', '%04d' % frame)
        elif '####' in file_path:
            evaluated_path3 = file_path.replace('####', '%04d' % frame)
        else:
            evaluated_path3 = file_path
        print("Manual substitution result: %s" % evaluated_path3)
    except Exception as e:
        print("Manual substitution failed: %s" % e)
        evaluated_path3 = None
    
    # Choose the best evaluated path
    final_path = evaluated_path1 or evaluated_path2 or evaluated_path3 or file_path
    print("Final output path: %s" % final_path)
    
    # Check if the directory exists
    output_dir = os.path.dirname(final_path)
    print("Output directory: %s" % output_dir)
    print("Directory exists: %s" % os.path.exists(output_dir))
    
    if not os.path.exists(output_dir):
        print("Creating directory...")
        try:
            os.makedirs(output_dir)
            print("Directory created successfully")
        except Exception as dir_e:
            print("ERROR creating directory: %s" % dir_e)
            sys.exit(1)
    
    # Force set the file path to ensure it's correct
    print("Setting Write node file path to: %s" % final_path)
    write_node['file'].setValue(final_path)
    
    # Execute the Write node for the specific frame
    print("Executing Write node for frame %d..." % frame)
    nuke.execute(write_node, frame, frame)
    
    print("Render completed successfully!")
    
    # Verify the output file was created
    if os.path.exists(final_path):
        file_size = os.path.getsize(final_path)
        print("SUCCESS: Output file created: %s (%d bytes)" % (final_path, file_size))
    else:
        print("WARNING: Could not find output file: %s" % final_path)
        # List files in the directory to see what was actually created
        try:
            files = os.listdir(output_dir)
            print("Files in output directory: %s" % files)
        except:
            print("Could not list files in output directory")
    
except Exception as e:
    print("ERROR during render: %s" % str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)
