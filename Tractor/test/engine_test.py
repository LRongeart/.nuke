#!/usr/bin/env python
"""
Basic Tractor Engine Test - Python 2.7 Compatible
==================================================

This script tests basic connectivity to Tractor engine using EngineClient
to help diagnose job pickup issues.
"""

import os
import sys

# Add local paths for Tractor API
script_dir = os.path.dirname(__file__)
tractor_path = os.path.join(script_dir, 'python2.7_portable', 'App', 'Python', 'Lib', 'site-packages')
if os.path.exists(tractor_path):
    sys.path.insert(0, tractor_path)
    print("[DEBUG] Added Tractor API path: " + tractor_path)

try:
    from tractor.base.EngineClient import EngineClient
    print("[SUCCESS] Tractor EngineClient is available")
    TRACTOR_AVAILABLE = True
except ImportError as e:
    print("[ERROR] Tractor EngineClient not available: " + str(e))
    TRACTOR_AVAILABLE = False

def test_engine_connection():
    """Test basic engine connectivity"""
    if not TRACTOR_AVAILABLE:
        print("[ERROR] Cannot test - Tractor API not available")
        return False
    
    try:
        print("\n" + "="*50)
        print("TESTING TRACTOR ENGINE CONNECTION")
        print("="*50)
        
        # Create EngineClient 
        ec = EngineClient()
        print("[INFO] EngineClient created successfully")
        
        # Try to get some basic info
        try:
            # Test if we can query anything
            print("[INFO] Testing engine connectivity...")
            
            # Try different query methods that might work
            methods_to_try = [
                ('blades', 'ec.blades()'),
                ('jobs', 'ec.jobs()'),
                ('query', 'ec.query("select * from blade")'),
            ]
            
            for method_name, method_call in methods_to_try:
                try:
                    print("[DEBUG] Trying " + method_name + "...")
                    if method_name == 'blades':
                        result = ec.blades()
                    elif method_name == 'jobs': 
                        result = ec.jobs()
                    elif method_name == 'query':
                        result = ec.query("select * from blade")
                    
                    print("[SUCCESS] " + method_name + " query worked!")
                    print("[INFO] Result type: " + str(type(result)))
                    print("[INFO] Result length: " + str(len(result) if hasattr(result, '__len__') else 'N/A'))
                    
                    if method_name == 'blades' and result:
                        print("\n[BLADE SUMMARY]:")
                        active_count = 0
                        total_count = len(result)
                        
                        for i, blade in enumerate(result[:5]):  # Show first 5 blades
                            name = blade.get('name', 'blade_' + str(i))
                            nimby = blade.get('nimby', 'unknown')
                            if nimby == 'off':
                                active_count += 1
                            print("  " + name + " (nimby: " + str(nimby) + ")")
                        
                        if total_count > 5:
                            print("  ... and " + str(total_count - 5) + " more blades")
                        
                        print("[SUMMARY] " + str(active_count) + "/" + str(total_count) + " blades are active")
                        
                        if active_count == 0:
                            print("[WARNING] No active blades found! This is why jobs aren't being picked up.")
                            print("[SOLUTION] Check blade status - they may be in 'nimby' mode or offline.")
                        elif active_count > 0:
                            print("[INFO] Active blades found. Job pickup issue may be due to:")
                            print("  - Service/envkey mismatch between jobs and blades")
                            print("  - Blade capacity (all slots busy)")
                            print("  - Job configuration errors")
                    
                    elif method_name == 'jobs' and result:
                        print("\n[RECENT JOBS SUMMARY]:")
                        for i, job in enumerate(result[:3]):  # Show first 3 jobs
                            jid = job.get('jid', 'unknown')
                            title = job.get('title', 'untitled')
                            state = job.get('state', 'unknown')
                            print("  Job " + str(jid) + ": " + title + " (" + state + ")")
                    
                    return True
                    
                except Exception as e:
                    print("[ERROR] " + method_name + " failed: " + str(e))
                    continue
            
            print("[ERROR] All query methods failed")
            return False
            
        except Exception as e:
            print("[ERROR] Engine queries failed: " + str(e))
            return False
            
    except Exception as e:
        print("[ERROR] Failed to create EngineClient: " + str(e))
        return False

def test_job_submission():
    """Test if we can submit a simple test job"""
    if not TRACTOR_AVAILABLE:
        return False
    
    try:
        print("\n" + "="*50)
        print("TESTING JOB SUBMISSION")
        print("="*50)
        
        # Create a simple test job TCL
        test_job_tcl = '''
Job {
    title "Tractor Diagnostics Test Job"
    priority 500
    service ""
    envkey {}
    crews {}
    maxactive 1
    
    Task {
        title "Test Task"
        id "test_task"
        
        Command {
            argv {"echo" "Hello from Tractor diagnostics test"}
        }
    }
}
'''
        
        print("[INFO] Creating test job with basic configuration...")
        print("[DEBUG] Job TCL:")
        print(test_job_tcl)
        
        ec = EngineClient()
        result = ec.spool(test_job_tcl, owner="TrackerUser", filename="diagnostics_test.alf")
        
        print("[SUCCESS] Test job submitted successfully!")
        print("[INFO] Job ID: " + str(result))
        print("[NOTE] This test job should be picked up by blades if they're properly configured")
        
        return True
        
    except Exception as e:
        print("[ERROR] Test job submission failed: " + str(e))
        return False

def main():
    print("Basic Tractor Engine Test (Python 2.7)")
    print("=" * 40)
    
    if not TRACTOR_AVAILABLE:
        print("\n[FATAL] Tractor API not available. Exiting.")
        return
    
    # Test engine connection
    connection_ok = test_engine_connection()
    
    if connection_ok:
        print("\n[SUCCESS] Engine connection test passed!")
        
        # Test job submission
        submission_ok = test_job_submission()
        
        if submission_ok:
            print("\n[SUCCESS] Job submission test passed!")
            print("\n[NEXT STEPS]:")
            print("1. Check Tractor web interface to see if the test job appears")
            print("2. Monitor if the test job gets picked up by blades")
            print("3. If test job works but your Nuke jobs don't, compare configurations")
        else:
            print("\n[PARTIAL SUCCESS] Engine works but job submission failed")
            print("Check Tractor configuration and permissions")
    else:
        print("\n[FAILURE] Engine connection test failed")
        print("Check:")
        print("- Tractor engine is running on simtracker:80")
        print("- Network connectivity")
        print("- Firewall settings")
        print("- Tractor configuration")
    
    print("\n" + "="*50)
    print("DIAGNOSTICS COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()
