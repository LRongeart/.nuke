#!/usr/bin/env python
"""
Simple Blade Status Check - Python 2.7
=======================================

Basic check to see what's available for job pickup
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
    print("SUCCESS: Tractor EngineClient imported")
    
    ec = EngineClient()
    print("SUCCESS: EngineClient created")
    
    # Try to submit a very simple test job to see if that works
    simple_test = '''Job {
    title "Quick Test"
    priority 500
    
    Task {
        title "Echo Test"
        Command {
            argv {"echo" "test"}
        }
    }
}'''
    
    print("Testing job submission...")
    result = ec.spool(simple_test, owner="TrackerUser")
    print("SUCCESS: Job submitted with ID " + str(result))
    print("")
    print("RECOMMENDATION FOR YOUR NUKE UI:")
    print("Since basic job submission works, try these settings:")
    print("  Service: '' (empty/blank)")
    print("  Envkey: '' (empty/blank)")  
    print("  Crews: '' (empty/blank)")
    print("  Priority: 500")
    print("  Owner: TrackerUser")
    print("")
    print("If this test job gets picked up but your Nuke jobs don't,")
    print("the issue is in your job configuration, not the blades.")
    
except Exception as e:
    print("ERROR: " + str(e))
    import traceback
    traceback.print_exc()
