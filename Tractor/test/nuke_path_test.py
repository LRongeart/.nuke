#!/usr/bin/env python
"""
Nuke Path Test - Test job submission with correct Nuke executable path
==================================================================

This script tests the updated Nuke executable path in a Tractor job
"""

import os
import sys

# Add local paths for Tractor API
script_dir = os.path.dirname(__file__)
tractor_path = os.path.join(script_dir, 'python2.7_portable', 'App', 'Python', 'Lib', 'site-packages')
if os.path.exists(tractor_path):
    sys.path.insert(0, tractor_path)

try:
    from tractor.base.EngineClient import EngineClient
    
    print("=== NUKE PATH TEST ===")
    
    ec = EngineClient()
    
    # Test using the new Nuke path format
    print("Testing with correct Nuke executable path...")
    
    # Create test job with new Nuke path
    nuke_path_test_job = '''##AlfredToDo 3.0
##
## Generated: Nuke Path Test Job
## Testing updated Nuke executable path

Job -title {Nuke Path Test} -project {EXIT} -priority 500 -maxactive {1} -service {PixarRender} -pause {0} -serialsubtasks 1 -subtasks {
    Task {Nuke Path Test} -serialsubtasks 0 -subtasks {
        Task {Test Nuke Path Frame 1001} -id {id0001} -cmds {
            RemoteCmd {"C:\\Program Files\\Nuke15.1v2\\Nuke15.1.exe"} {"--nukex" "--version"} -service {"PixarRender"} -envkey {} -refersto {"id0001"} 
        }
    }
}'''
    
    try:
        result = ec.spool(nuke_path_test_job, owner="TrackerUser", filename="nuke_path_test.alf")
        print("SUCCESS: " + str(result))
        if '"jid": ' in str(result):
            job_id = str(result).split('"jid": ')[1].split('}')[0]
            print("Job ID: " + job_id)
            print("Check this job in Tractor web interface to verify Nuke path works")
        
    except Exception as e:
        print("FAILED: " + str(e))
        
    print("\n=== END NUKE PATH TEST ===")
    
except ImportError as e:
    print("ERROR: Could not import Tractor modules: " + str(e))
    sys.exit(1)
