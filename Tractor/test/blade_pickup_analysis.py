#!/usr/bin/env python
"""
Blade Pickup Analysis
====================

This script analyzes why jobs appear in Tractor but aren't picked up by blades.
We'll check the job in the queue and compare it to blade capabilities.
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
    print("SUCCESS: Connected to Tractor")
    
    # Let's try using the select method for direct database queries
    ec = EngineClient()
    
    print("\n=== CHECKING JOB QUEUE ===")
    
    # Query jobs that are ready but not picked up
    try:
        ready_jobs = ec.select("select jid, title, state, service, envkey, crews, owner, priority from job where state='ready' order by spooltime desc limit 5")
        print("Ready jobs waiting for pickup:")
        
        if ready_jobs:
            for job in ready_jobs:
                jid, title, state, service, envkey, crews, owner, priority = job
                print("  Job " + str(jid) + ": " + str(title))
                print("    State: " + str(state))
                print("    Service: '" + str(service) + "'")
                print("    Envkey: '" + str(envkey) + "'")
                print("    Crews: '" + str(crews) + "'")
                print("    Owner: " + str(owner))
                print("    Priority: " + str(priority))
                print()
        else:
            print("  No ready jobs found")
            
    except Exception as e:
        print("ERROR querying jobs: " + str(e))
    
    print("\n=== CHECKING ACTIVE BLADES ===")
    
    # Query active blades and their current status
    try:
        # Check blade status and what they're looking for
        active_blades = ec.select("select name, nimby, numslots, availslots, profile from blade where nimby='off' limit 10")
        print("Active blades (first 10):")
        
        if active_blades:
            for blade in active_blades:
                name, nimby, numslots, availslots, profile = blade
                print("  Blade: " + str(name))
                print("    Slots: " + str(availslots) + "/" + str(numslots) + " available")
                print("    Profile: " + str(profile))
                print()
        else:
            print("  No active blades found")
            
    except Exception as e:
        print("ERROR querying blades: " + str(e))
    
    print("\n=== DIAGNOSIS ===")
    print("If you see:")
    print("1. Ready jobs + Active blades with slots = Configuration mismatch")
    print("2. Ready jobs + No available slots = Capacity issue")
    print("3. No ready jobs = Jobs are being picked up (check running/done jobs)")
    print("4. No active blades = Blade configuration issue")
    
    print("\n=== QUICK FIX TEST ===")
    print("Submitting ultra-simple test job...")
    
    # Submit the most basic possible job
    minimal_job = '''Job {
    title "Minimal Test Job"
    priority 1000
    
    Task {
        title "Simple Echo"
        Command {
            argv {"echo" "minimal test"}
        }
    }
}'''
    
    try:
        result = ec.spool(minimal_job, owner="TrackerUser")
        print("SUCCESS: Minimal test job submitted with ID " + str(result))
        print("Check if this minimal job gets picked up.")
        print("If it does, the issue is in your Nuke job configuration.")
        print("If it doesn't, the issue is with blade matching logic.")
    except Exception as e:
        print("ERROR: Could not submit test job: " + str(e))
        
except Exception as e:
    print("ERROR: " + str(e))
    import traceback
    traceback.print_exc()
