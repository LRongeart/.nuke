#!/usr/bin/env python
"""
Tractor Job for Plugin Loading Diagnostic

This creates a simple Tractor job that will run on the render farm
to diagnose exactly why Connect.gizmo isn't loading properly.
"""

import sys
import os

# Add the tractor module path
sys.path.insert(0, r'\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor')

def create_diagnostic_job():
    """Create a Tractor job to run plugin diagnostic on render farm"""
    
    # Import our bridge function
    from tractor_spool_bridge import spool_job_via_bridge
    
    # Create a simple Nuke script that runs our diagnostic
    diagnostic_script_content = '''# Plugin Diagnostic Script
set cut_paste_input [stack 0]
version 15.1 v2
Constant {
 inputs 0
 color {1 0 0 1}
 name Constant1
 selected true
 xpos 0
 ypos 0
}
Write {
 file "//tls-storage02/Install/NUKE/Nuke_PLUG/.nuke_DEV/tractor/diagnostic_output.####.exr"
 name Write1
 selected true
 xpos 0
 ypos 100
}
'''
    
    # Save the diagnostic script
    script_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\plugin_diagnostic.nk"
    with open(script_path, 'w') as f:
        f.write(diagnostic_script_content)
    
    # Create Tractor job
    job_data = f'''##AlfredToDo 3.0
Job -title "Plugin Loading Diagnostic" -service PixarRender -crews {{any}} -envkey {{}} -comment "Diagnose Connect.gizmo loading issue" -maxactive 1 {{
    Task -title "Diagnostic" {{
        Cmd -service PixarRender -msg "Running plugin diagnostic" {{
            "C:\\Program Files\\Nuke15.1v2\\Nuke15.1.exe" -t "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke_DEV\\tractor\\plugin_loading_diagnostic.py"
        }}
    }}
}}'''
    
    print("Creating diagnostic job...")
    try:
        result = spool_job_via_bridge(job_data, owner="3d4", filename="plugin_diagnostic.alf")
        print(f"Diagnostic job submitted: {result}")
        print("\nNext steps:")
        print("1. Check Tractor web interface for job completion")
        print("2. Review job logs to see diagnostic output")
        print("3. Based on results, we'll implement the appropriate fix")
        return True
    except Exception as e:
        print(f"Failed to submit diagnostic job: {e}")
        return False

if __name__ == "__main__":
    create_diagnostic_job()
