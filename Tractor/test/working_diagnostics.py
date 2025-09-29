#!/usr/bin/env python
"""
Working Tractor Diagnostics - Python 2.7 Compatible
===================================================

This script uses the actual EngineClient methods to diagnose Tractor issues.
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
    print("[SUCCESS] Tractor EngineClient imported")
    TRACTOR_AVAILABLE = True
except ImportError as e:
    print("[ERROR] Tractor EngineClient not available: " + str(e))
    TRACTOR_AVAILABLE = False

def analyze_blades():
    """Analyze blade status and capabilities"""
    try:
        print("\n" + "="*60)
        print("BLADE ANALYSIS")
        print("="*60)
        
        ec = EngineClient()
        
        # Fetch blades as JSON
        blades_json = ec.fetchBladesAsJSON()
        print("[INFO] Raw blades JSON length: " + str(len(blades_json)))
        
        # Parse the JSON (it should be a string)
        import json
        blades_data = json.loads(blades_json)
        
        blades = blades_data.get('data', []) if isinstance(blades_data, dict) else blades_data
        
        print("[INFO] Found " + str(len(blades)) + " total blades")
        
        if not blades:
            print("[WARNING] No blades found!")
            return []
        
        active_count = 0
        available_services = set()
        available_envkeys = set()
        blade_summary = []
        
        for blade in blades:
            name = blade.get('name', 'unknown')
            nimby = blade.get('nimby', 'unknown')
            profile = blade.get('profile', {})
            capacity = blade.get('capacity', 1)
            availcapacity = blade.get('availcapacity', 0)
            
            services = profile.get('service', [])
            envkeys = profile.get('envkey', [])
            crews = profile.get('crews', [])
            
            if nimby == 'off':
                active_count += 1
                if availcapacity > 0:
                    available_services.update(services)
                    available_envkeys.update(envkeys)
            
            blade_info = {
                'name': name,
                'active': nimby == 'off',
                'available': availcapacity > 0,
                'services': services,
                'envkeys': envkeys,
                'crews': crews,
                'capacity': str(capacity),
                'availcapacity': str(availcapacity)
            }
            blade_summary.append(blade_info)
            
            status = "ACTIVE" if nimby == 'off' else "NIMBY"
            if nimby == 'off' and availcapacity == 0:
                status += " (BUSY)"
            
            print("\nBlade: " + name)
            print("  Status: " + status)
            print("  Capacity: " + str(capacity) + " (available: " + str(availcapacity) + ")")
            print("  Services: " + str(services))
            print("  Envkeys: " + str(envkeys))
            print("  Crews: " + str(crews))
        
        print("\n" + "="*40)
        print("BLADE SUMMARY")
        print("="*40)
        print("Total blades: " + str(len(blades)))
        print("Active blades (nimby=off): " + str(active_count))
        print("Available services: " + str(list(available_services)))
        print("Available envkeys: " + str(list(available_envkeys)))
        
        if active_count == 0:
            print("\n[CRITICAL] NO ACTIVE BLADES!")
            print("This is why jobs are not being picked up.")
            print("Solution: Check blade configuration and activate them.")
        elif len(available_services) == 0:
            print("\n[WARNING] No services available on active blades!")
            print("Jobs with specific service requirements won't be picked up.")
        
        return blade_summary
        
    except Exception as e:
        print("[ERROR] Failed to analyze blades: " + str(e))
        import traceback
        traceback.print_exc()
        return []

def analyze_jobs():
    """Analyze recent job status"""
    try:
        print("\n" + "="*60)
        print("RECENT JOBS ANALYSIS")
        print("="*60)
        
        ec = EngineClient()
        
        # Fetch recent jobs as JSON
        jobs_json = ec.fetchJobsAsJSON()
        print("[INFO] Raw jobs JSON length: " + str(len(jobs_json)))
        
        # Parse the JSON
        import json
        jobs_data = json.loads(jobs_json)
        
        jobs = jobs_data.get('data', []) if isinstance(jobs_data, dict) else jobs_data
        
        # Limit to recent jobs (first 10)
        recent_jobs = jobs[:10] if len(jobs) > 10 else jobs
        
        print("[INFO] Found " + str(len(jobs)) + " total jobs, showing " + str(len(recent_jobs)) + " recent ones")
        
        if not recent_jobs:
            print("[WARNING] No recent jobs found!")
            return []
        
        working_configs = []
        
        for job in recent_jobs:
            jid = job.get('jid', 'unknown')
            title = job.get('title', 'untitled')[:50]  # Truncate long titles
            owner = job.get('owner', 'unknown')
            state = job.get('state', 'unknown')
            service = job.get('service', '')
            envkey = job.get('envkey', [])
            crews = job.get('crews', [])
            priority = job.get('priority', 0)
            
            print("\nJob " + str(jid) + ": " + title)
            print("  Owner: " + owner)
            print("  State: " + state)
            print("  Service: '" + str(service) + "'")
            print("  Envkey: " + str(envkey))
            print("  Crews: " + str(crews))
            print("  Priority: " + str(priority))
            
            if state in ['done', 'active']:
                working_configs.append({
                    'service': service,
                    'envkey': envkey,
                    'crews': crews,
                    'state': state,
                    'priority': priority
                })
        
        if working_configs:
            print("\n" + "="*40)
            print("WORKING JOB CONFIGURATIONS")
            print("="*40)
            for i, config in enumerate(working_configs):
                print("Config " + str(i+1) + ":")
                print("  Service: '" + str(config['service']) + "'")
                print("  Envkey: " + str(config['envkey']))
                print("  Crews: " + str(config['crews']))
                print("  State: " + config['state'])
        
        return recent_jobs
        
    except Exception as e:
        print("[ERROR] Failed to analyze jobs: " + str(e))
        import traceback
        traceback.print_exc()
        return []

def recommend_nuke_config(blades, jobs):
    """Recommend best Nuke job configuration"""
    print("\n" + "="*60)
    print("NUKE CONFIGURATION RECOMMENDATIONS")
    print("="*60)
    
    if not blades:
        print("[ERROR] No blade data available")
        return
    
    # Find active blades with capacity
    active_blades = []
    for blade in blades:
        if blade['active'] and int(blade['availcapacity']) > 0:
            active_blades.append(blade)
    
    if not active_blades:
        print("[CRITICAL] No active blades with available capacity!")
        print("Solutions:")
        print("1. Wait for current jobs to finish")
        print("2. Activate more blades")
        print("3. Check blade configuration")
        return
    
    print("[INFO] Found " + str(len(active_blades)) + " active blades with capacity")
    
    # Collect all available services and envkeys
    all_services = set()
    all_envkeys = set()
    
    for blade in active_blades:
        all_services.update(blade['services'])
        all_envkeys.update(blade['envkeys'])
    
    print("[INFO] Available services: " + str(list(all_services)))
    print("[INFO] Available envkeys: " + str(list(all_envkeys)))
    
    # Test different Nuke configurations
    test_configs = [
        {'name': 'No Service (Default)', 'service': '', 'envkey': []},
        {'name': 'NukeXRender + rez', 'service': 'NukeXRender', 'envkey': ['rez']},
        {'name': 'NukeRender + rez', 'service': 'NukeRender', 'envkey': ['rez']},
        {'name': 'NukeXRender only', 'service': 'NukeXRender', 'envkey': []},
        {'name': 'NukeRender only', 'service': 'NukeRender', 'envkey': []},
    ]
    
    best_config = None
    best_count = 0
    
    for config in test_configs:
        compatible_count = 0
        
        for blade in active_blades:
            service_ok = True
            envkey_ok = True
            
            # Check service compatibility
            if config['service']:
                service_ok = config['service'] in blade['services']
            
            # Check envkey compatibility
            if config['envkey']:
                envkey_ok = any(ek in blade['envkeys'] for ek in config['envkey'])
            
            if service_ok and envkey_ok:
                compatible_count += 1
        
        status = "WORKS" if compatible_count > 0 else "FAILS"
        print("\n" + config['name'] + ": " + status + " (" + str(compatible_count) + " compatible blades)")
        
        if compatible_count > best_count:
            best_count = compatible_count
            best_config = config
    
    if best_config:
        print("\n" + "="*40)
        print("RECOMMENDED CONFIGURATION")
        print("="*40)
        print("Use these settings in your Nuke UI:")
        print("  Service: '" + str(best_config['service']) + "'")
        print("  Envkey: " + str(best_config['envkey']))
        print("  Crews: []")
        print("  Priority: 500")
        print("  Owner: TrackerUser")
        print("\nThis configuration should work with " + str(best_count) + " blade(s)")
    else:
        print("\n[ERROR] NO WORKING CONFIGURATION FOUND!")
        print("All test configurations failed. Check blade services and envkeys.")

def test_job_submission():
    """Test submitting a simple job"""
    try:
        print("\n" + "="*60)
        print("TEST JOB SUBMISSION")
        print("="*60)
        
        # Create a simple test job
        test_job_tcl = '''Job {
    title "Diagnostics Test Job"
    priority 500
    service ""
    envkey {}
    crews {}
    maxactive 1
    
    Task {
        title "Test Echo Command"
        id "test_echo"
        
        Command {
            argv {"echo" "Hello from Tractor diagnostics test"}
        }
    }
}'''
        
        print("[INFO] Submitting test job...")
        
        ec = EngineClient()
        result = ec.spool(test_job_tcl, owner="TrackerUser", filename="diagnostics_test.alf")
        
        print("[SUCCESS] Test job submitted!")
        print("[INFO] Job ID: " + str(result))
        print("\n[NEXT STEPS]:")
        print("1. Check Tractor web interface for job ID " + str(result))
        print("2. Monitor if this test job gets picked up by blades")
        print("3. If this works but your Nuke jobs don't, compare job configurations")
        
        return True
        
    except Exception as e:
        print("[ERROR] Test job submission failed: " + str(e))
        return False

def main():
    print("Working Tractor Diagnostics Tool")
    print("=" * 35)
    
    if not TRACTOR_AVAILABLE:
        print("\n[FATAL] Tractor API not available. Exiting.")
        return
    
    # Analyze blades
    blades = analyze_blades()
    
    # Analyze recent jobs
    jobs = analyze_jobs()
    
    # Recommend configuration
    recommend_nuke_config(blades, jobs)
    
    # Test job submission
    test_job_submission()
    
    print("\n" + "="*60)
    print("DIAGNOSTICS COMPLETE")
    print("="*60)
    
    print("\nSUMMARY:")
    print("- Blade analysis: " + ("DONE" if blades else "FAILED"))
    print("- Job analysis: " + ("DONE" if jobs else "FAILED"))
    print("- Check the recommendations above to fix job pickup issues")

if __name__ == "__main__":
    main()
