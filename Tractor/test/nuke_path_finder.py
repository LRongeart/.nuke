#!/usr/bin/env python3
"""
Nuke Path Finder for Render Blades
This script creates a Tractor job to test different Nuke executable paths on render blades.
"""

import os
import sys
import json
import subprocess

def spool_job_via_bridge(job_data, owner="3d4", filename=None):
    """Spool a job through the Python 2.7 bridge"""
    python2_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\python2.7_portable\App\Python\python.exe"
    bridge_script = r"//tls-storage02/Install/NUKE/Nuke_PLUG/.nuke_DEV/tractor/tractor_spool_bridge.py"

    cmd_args = [python2_path, bridge_script, owner]
    if filename:
        cmd_args.append(filename)

    proc = subprocess.Popen(
        cmd_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = proc.communicate(input=job_data.encode('utf-8'))
    if proc.returncode != 0:
        raise RuntimeError("Bridge error: " + err.decode('utf-8'))
    return json.loads(out.decode('utf-8'))["result"]

def create_nuke_path_test_job():
    """Create a test job to find Nuke on render blades"""
    
    # Possible Nuke paths to test
    nuke_paths = [
        "nuke.exe",  # Default in PATH
        "nuke",      # Linux/Unix style
        r"C:\Program Files\Nuke15.1v1\nuke.exe",
        r"C:\Program Files\Nuke14.0v5\nuke.exe", 
        r"C:\Program Files\Nuke13.2v7\nuke.exe",
        r"C:\Program Files\Nuke12.2v10\nuke.exe",
        r"C:\Program Files\Foundry\Nuke15.1v1\nuke.exe",
        r"C:\Program Files\Foundry\Nuke14.0v5\nuke.exe",
        r"C:\Program Files\Foundry\Nuke13.2v7\nuke.exe",
        r"\\tls-storage02\Install\NUKE\Nuke15.1v1\nuke.exe",
        r"\\tls-storage02\Install\NUKE\Nuke14.0v5\nuke.exe",
        r"\\tls-storage02\Install\NUKE\Nuke13.2v7\nuke.exe",
        r"\\tls-storage02\Install\FOUNDRY\Nuke15.1v1\nuke.exe",
        r"\\tls-storage02\Install\FOUNDRY\Nuke14.0v5\nuke.exe",
    ]
    
    # Create the job data (ALF format)
    job_data = '''##AlfredToDo 3.0
##
## Nuke Path Test Job

Job -title {Nuke Path Test} -project {TEST} -priority 1.0 -maxactive {1} -service {PixarRender} -pause {0} -serialsubtasks 1 -subtasks {
    Task {Nuke Path Tests} -serialsubtasks 0 -subtasks {
'''

    # Add a test task for each possible Nuke path
    for i, nuke_path in enumerate(nuke_paths, 1):
        # Escape quotes in path for ALF format
        escaped_path = nuke_path.replace('"', '\\"')
        
        # Create a simple test command that just tries to run nuke --version
        job_data += f'''        Task {{Test Path {i}: {escaped_path}}} -id {{id{i:04d}}} -cmds {{
            RemoteCmd {{cmd.exe}} {{"/c"}} {{"{escaped_path} --version > nuke_version_{i}.txt 2>&1 || echo FAILED: {escaped_path} > nuke_version_{i}.txt"}} -service {{"PixarRender"}} -envkey {{}} -refersto {{id{i:04d}}}
        }}
'''

    # Close the job structure
    job_data += '''    }
}
'''
    
    return job_data

def main():
    """Main function to create and submit the Nuke path test job"""
    try:
        print("Creating Nuke path test job...")
        job_data = create_nuke_path_test_job()
        
        print("Submitting job via bridge...")
        result = spool_job_via_bridge(job_data, owner="3d4", filename="nuke_path_test.alf")
        
        print(f"Job submitted successfully!")
        print(f"Job ID: {result}")
        print("")
        print("This job will test multiple Nuke executable paths on render blades.")
        print("Check the Tractor web interface for results.")
        print("Look for output files like 'nuke_version_*.txt' to see which paths work.")
        
    except Exception as e:
        print(f"Error submitting job: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
