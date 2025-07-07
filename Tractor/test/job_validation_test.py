#!/usr/bin/env python
"""
Job Submission Validation Test
=============================

Test why jobs get "accepted" but don't appear in Tractor queue
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
    
    print("=== JOB SUBMISSION VALIDATION TEST ===")
    
    ec = EngineClient()
    
    # Test 1: Copy exact format from working example
    print("\nTest 1: Using exact format from working example...")
    
    working_job = '''Job {
    title "Working Format Test"
    priority 500
    crews {}
    service ""
    envkey {}
    maxactive 1
    serialsubtasks 1
    
    Task {
        title "Test Task"
        id "test_task_1"
        
        Command {
            argv {"echo" "working format test"}
        }
    }
}'''
    
    try:
        result1 = ec.spool(working_job, owner="TrackerUser", filename="working_test.alf")
        print("SUCCESS Test 1: " + str(result1))
        job_id_1 = str(result1).split('"jid": ')[1].split('}')[0] if '"jid": ' in str(result1) else "unknown"
        print("Job ID to check: " + job_id_1)
    except Exception as e:
        print("FAILED Test 1: " + str(e))
    
    # Test 2: Even simpler job
    print("\nTest 2: Ultra minimal job...")
    
    minimal_job = '''Job {
    title "Ultra Minimal"
    
    Task {
        title "Echo"
        Command {
            argv {"echo" "test"}
        }
    }
}'''
    
    try:
        result2 = ec.spool(minimal_job, owner="TrackerUser", filename="minimal_test.alf")
        print("SUCCESS Test 2: " + str(result2))
        job_id_2 = str(result2).split('"jid": ')[1].split('}')[0] if '"jid": ' in str(result2) else "unknown"
        print("Job ID to check: " + job_id_2)
    except Exception as e:
        print("FAILED Test 2: " + str(e))
    
    # Test 3: Check what happens with bad job
    print("\nTest 3: Intentionally bad job...")
    
    bad_job = '''Job {
    title "Bad Job Test"
    invalid_attribute "this should fail"
    
    Task {
        title "Bad Task"
        Command {
            argv {"echo" "bad test"}
        }
    }
}'''
    
    try:
        result3 = ec.spool(bad_job, owner="TrackerUser", filename="bad_test.alf")
        print("SUCCESS Test 3 (unexpected): " + str(result3))
    except Exception as e:
        print("FAILED Test 3 (expected): " + str(e))
    
    print("\n=== RESULTS ===")
    print("Check Tractor web interface for these job IDs:")
    try:
        print("- Test 1 (working format): " + job_id_1)
    except:
        print("- Test 1: submission failed")
    try:
        print("- Test 2 (minimal): " + job_id_2)
    except:
        print("- Test 2: submission failed")
    
    print("\nIf NONE of these jobs appear in Tractor:")
    print("1. Jobs are being rejected after 'acceptance'")
    print("2. Check Tractor engine logs for validation errors")
    print("3. May be authentication/permission issue")
    print("4. Could be network/database connectivity issue")
    
    print("\nIf some jobs appear but others don't:")
    print("- Compare working vs non-working job formats")
    print("- Focus on job attributes that cause rejection")
    
except Exception as e:
    print("ERROR: " + str(e))
    import traceback
    traceback.print_exc()
