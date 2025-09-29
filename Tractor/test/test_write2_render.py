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
    
    # Check Write node file path
    file_path = write_node['file'].value()
    print("Write node file path: %s" % file_path)
    
    if not file_path or file_path.strip() == "":
        print("ERROR: Write node '%s' has no output file path" % write_name)
        sys.exit(1)
    
    # Try to get the evaluated filename for the current frame
    try:
        frame = 1
        nuke.frame(frame)  # Set current frame
        evaluated_path = nuke.filename(write_node)
        print("Evaluated path for frame %d: %s" % (frame, evaluated_path))
        
        # Check if the directory exists
        output_dir = os.path.dirname(evaluated_path)
        if not os.path.exists(output_dir):
            print("ERROR: Output directory does not exist: %s" % output_dir)
            print("Creating directory...")
            try:
                os.makedirs(output_dir)
                print("Directory created successfully")
            except Exception as dir_e:
                print("ERROR creating directory: %s" % dir_e)
                sys.exit(1)
        
    except Exception as eval_e:
        print("WARNING: Could not evaluate path: %s" % eval_e)
        evaluated_path = file_path
    
    # Execute the Write node for the specific frame
    frame = 1
    print("Rendering frame %d from Write node '%s'" % (frame, write_name))
    nuke.execute(write_node, frame, frame)
    
    print("Frame %d completed successfully" % frame)
    
    # Verify the output file was created
    if evaluated_path and os.path.exists(evaluated_path):
        file_size = os.path.getsize(evaluated_path)
        print("Output file created: %s (%d bytes)" % (evaluated_path, file_size))
    else:
        print("WARNING: Could not verify output file: %s" % evaluated_path)
    
except Exception as e:
    print("ERROR during render: %s" % str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)
