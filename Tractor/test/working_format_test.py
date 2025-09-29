#!/usr/bin/env python
"""
Working Format Test - Submit using exact working example format
============================================================

Test job submission using the exact format from the working example
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
    
    print("=== WORKING FORMAT TEST ===")
    
    ec = EngineClient()
    
    # Test using ALF format that matches the working example exactly
    print("Testing with ALF format matching working example...")
    
    # Note: Using ALF format, not TCL format
    working_alf_job = '''##AlfredToDo 3.0
##
## Generated: Test Job
## Nuke Render Test

Job -title {Nuke Test Job} -project {EXIT} -priority 500 -maxactive {1} -service {PixarRender} -pause {0} -serialsubtasks 1 -subtasks {
    Task {Nuke Render} -serialsubtasks 0 -subtasks {
        Task {Nuke Render Frame 1001} -id {id0001} -cmds {
            RemoteCmd {echo} {"test nuke render frame 1001"} -service {"PixarRender"} -envkey {} -refersto {"id0001"} 
        }
    }
}'''
    
    try:
        result1 = ec.spool(working_alf_job, owner="TrackerUser", filename="working_format_test.alf")
        print("SUCCESS ALF format: " + str(result1))
        if '"jid": ' in str(result1):
            job_id = str(result1).split('"jid": ')[1].split('}')[0]
            print("Check for Job ID: " + job_id + " in Tractor web interface")
        
    except Exception as e:
        print("FAILED ALF format: " + str(e))
    
    # Test 2: Try different service from your environment
    print("\nTesting with different services...")
    
    services_to_try = ['', 'NukeRender', 'NukeXRender', 'generic']
    
    for service in services_to_try:
        print("Trying service: '" + str(service) + "'")
        
        test_job = '''Job {
    title "Service Test ''' + str(service) + '''"
    priority 500
    service "''' + service + '''"
    envkey {}
    maxactive 1
    
    Task {
        title "Test Task"
        Command {
            argv {"echo" "service test"}
        }
    }
}'''
        
        try:
            result = ec.spool(test_job, owner="TrackerUser", filename="service_test_" + str(service).replace(' ', '_') + ".alf")
            print("  SUCCESS: " + str(result))
            if '"jid": ' in str(result):
                job_id = str(result).split('"jid": ')[1].split('}')[0]
                print("  Job ID: " + job_id)
        except Exception as e:
            print("  FAILED: " + str(e))
    
    print("\n=== CHECK RESULTS ===")
    print("Look in Tractor web interface for any of these test jobs")
    print("If working format appears but others don't:")
    print("- Your system requires specific service (PixarRender)")
    print("- May need ALF format instead of TCL")
    print("- Project field may be required")
    
except Exception as e:
    print("ERROR: " + str(e))
    import traceback
    traceback.print_exc()
