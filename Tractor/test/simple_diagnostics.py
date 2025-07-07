#!/usr/bin/env python
"""
Simple Tractor Diagnostics - Python 2.7 Compatible
===================================================

This script provides basic Tractor farm diagnostics using Python 2.7
compatible syntax for use with the local Tractor installation.
"""

import os
import sys
import json

# Add local paths for Tractor API
script_dir = os.path.dirname(__file__)
tractor_paths = [
    script_dir,
    os.path.join(script_dir, 'python2.7_portable', 'App', 'Python', 'Lib', 'site-packages'),
]

for path in tractor_paths:
    if os.path.exists(path):
        sys.path.insert(0, path)
        print("[DEBUG] Added to Python path: " + path)

try:
    # Use the same import approach as the working bridge script
    from tractor.base.EngineClient import EngineClient
    print("[SUCCESS] Tractor EngineClient is available")
    TRACTOR_AVAILABLE = True
except ImportError as e:
    print("[ERROR] Tractor API not available: " + str(e))
    TRACTOR_AVAILABLE = False

# Configuration
SIMTRACKER = {
    "host": "simtracker", 
    "port": 80,
    "user": "TrackerUser",
    "password": "TrackerUser"
}

def connect_to_engine():
    """Connect to Tractor engine"""
    try:
        print("[INFO] Connecting to Tractor engine at " + SIMTRACKER['host'] + ":" + str(SIMTRACKER['port']))
        tq.setEngineClientParam(
            hostname=SIMTRACKER["host"],
            port=SIMTRACKER["port"],
            user=SIMTRACKER["user"],
            password=SIMTRACKER["password"]
        )
        
        # Test connection with a simple query that doesn't require search clauses
        try:
            # Try to get engine info first
            engine_info = tq.engine()
            print("[SUCCESS] Connected to Tractor engine successfully")
            print("[INFO] Engine version: " + str(engine_info.get('version', 'unknown')))
            return True
        except Exception as e:
            # If engine() fails, try a simple jobs query with empty search
            print("[DEBUG] engine() failed, trying jobs query: " + str(e))
            jobs = tq.jobs(limit=1, sortby=[['spooltime', -1]])
            print("[SUCCESS] Connected to Tractor engine successfully (via jobs query)")
            return True
        
    except Exception as e:
        print("[ERROR] Failed to connect to Tractor engine: " + str(e))
        return False

def query_blades():
    """Query all available blades"""
    try:
        print("\n" + "="*60)
        print("BLADE ANALYSIS")
        print("="*60)
        
        blades = tq.blades()
        blade_count = len(blades) if blades else 0
        print("[INFO] Found " + str(blade_count) + " total blades")
        
        if not blades:
            print("[WARNING] No blades found!")
            return []
        
        active_count = 0
        nuke_services = set()
        all_envkeys = set()
        
        for i, blade in enumerate(blades):
            blade_name = blade.get('name', 'blade_' + str(i))
            nimby = blade.get('nimby', 'unknown')
            profile = blade.get('profile', {})
            
            services = profile.get('service', [])
            envkeys = profile.get('envkey', [])
            crews = profile.get('crews', [])
            capacity = blade.get('capacity', 1)
            availcapacity = blade.get('availcapacity', 0)
            
            if nimby == 'off':
                active_count += 1
                
            print("\nBlade: " + blade_name)
            print("  Status: " + ("ACTIVE" if nimby == 'off' else "NIMBY"))
            print("  Services: " + str(services))
            print("  Envkeys: " + str(envkeys))
            print("  Crews: " + str(crews))
            print("  Capacity: " + str(capacity) + " (available: " + str(availcapacity) + ")")
            
            # Collect service and envkey information
            nuke_services.update(services)
            all_envkeys.update(envkeys)
        
        print("\n[SUMMARY] " + str(active_count) + "/" + str(len(blades)) + " blades are active (nimby=off)")
        print("[SUMMARY] Available services: " + str(list(nuke_services)))
        print("[SUMMARY] Available envkeys: " + str(list(all_envkeys)))
        
        return blades
        
    except Exception as e:
        print("[ERROR] Failed to query blades: " + str(e))
        import traceback
        traceback.print_exc()
        return []

def query_recent_jobs(limit=5):
    """Query recent jobs"""
    try:
        print("\n" + "="*60)
        print("RECENT JOBS ANALYSIS")
        print("="*60)
        
        # Use proper search parameters for jobs query
        jobs = tq.jobs(limit=limit, sortby=[['spooltime', -1]])
        job_count = len(jobs) if jobs else 0
        print("[INFO] Found " + str(job_count) + " recent jobs")
        
        if not jobs:
            print("[WARNING] No recent jobs found!")
            return []
        
        working_configs = []
        
        for job in jobs:
            jid = job.get('jid', 'unknown')
            title = job.get('title', 'untitled')
            owner = job.get('owner', 'unknown')
            state = job.get('state', 'unknown')
            service = job.get('service', 'none')
            envkey = job.get('envkey', [])
            crews = job.get('crews', [])
            
            print("\nJob " + str(jid) + ": " + title)
            print("  Owner: " + owner)
            print("  State: " + state)
            print("  Service: " + str(service))
            print("  Envkey: " + str(envkey))
            print("  Crews: " + str(crews))
            
            if state in ['done', 'active']:
                working_configs.append({
                    'service': service,
                    'envkey': envkey,
                    'crews': crews,
                    'state': state
                })
        
        if working_configs:
            print("\n[WORKING CONFIGURATIONS]:")
            for config in working_configs:
                print("  Service: " + str(config['service']) + ", Envkey: " + str(config['envkey']) + ", State: " + config['state'])
        
        return jobs
        
    except Exception as e:
        print("[ERROR] Failed to query jobs: " + str(e))
        import traceback
        traceback.print_exc()
        return []

def analyze_nuke_configs(blades):
    """Analyze which Nuke configurations will work"""
    if not blades:
        print("\n[ERROR] No blade data available for analysis")
        return
    
    print("\n" + "="*60)
    print("NUKE JOB CONFIGURATION ANALYSIS")
    print("="*60)
    
    # Extract available services and envkeys from active blades
    available_services = set()
    available_envkeys = set()
    active_blades = []
    
    for blade in blades:
        if blade.get('nimby') == 'off' and blade.get('availcapacity', 0) > 0:
            active_blades.append(blade)
            profile = blade.get('profile', {})
            available_services.update(profile.get('service', []))
            available_envkeys.update(profile.get('envkey', []))
    
    print("[INFO] Active blades with capacity: " + str(len(active_blades)))
    print("[INFO] Available services: " + str(list(available_services)))
    print("[INFO] Available envkeys: " + str(list(available_envkeys)))
    
    # Test common Nuke configurations
    test_configs = [
        {'name': 'NukeXRender + rez', 'service': 'NukeXRender', 'envkey': ['rez']},
        {'name': 'NukeRender + rez', 'service': 'NukeRender', 'envkey': ['rez']},
        {'name': 'NukeXRender only', 'service': 'NukeXRender', 'envkey': []},
        {'name': 'NukeRender only', 'service': 'NukeRender', 'envkey': []},
        {'name': 'No service', 'service': None, 'envkey': []},
        {'name': 'Generic service', 'service': 'generic', 'envkey': []},
    ]
    
    working_configs = []
    
    for config in test_configs:
        compatible_count = 0
        
        for blade in active_blades:
            profile = blade.get('profile', {})
            blade_services = profile.get('service', [])
            blade_envkeys = profile.get('envkey', [])
            
            # Check service compatibility
            service_ok = True
            if config['service']:
                service_ok = config['service'] in blade_services
            
            # Check envkey compatibility  
            envkey_ok = True
            if config['envkey']:
                envkey_ok = any(ek in blade_envkeys for ek in config['envkey'])
            
            if service_ok and envkey_ok:
                compatible_count += 1
        
        status = "WORKING" if compatible_count > 0 else "NOT WORKING"
        print("\n" + config['name'] + ": " + status + " (" + str(compatible_count) + " compatible blades)")
        
        if compatible_count > 0:
            working_configs.append(config)
    
    if working_configs:
        print("\n" + "="*40)
        print("RECOMMENDED CONFIGURATIONS:")
        print("="*40)
        
        best_config = max(working_configs, key=lambda c: len([b for b in active_blades if is_compatible(b, c)]))
        
        print("\nBest configuration:")
        print("  Service: " + str(best_config.get('service', 'None')))
        print("  Envkey: " + str(best_config.get('envkey', [])))
        print("  Crews: []")
        print("  Owner: TrackerUser")
        print("  Priority: 500")
        
        print("\nTo use in your Nuke UI:")
        print("1. Set Service to: " + str(best_config.get('service', 'None')))
        print("2. Set Envkey to: " + str(best_config.get('envkey', [])))
        print("3. Submit your job")
        
    else:
        print("\n[ERROR] NO WORKING CONFIGURATIONS FOUND!")
        print("This means:")
        print("- No blades are active with available capacity, OR")
        print("- Blade services/envkeys don't match common Nuke requirements")
        print("\nCheck blade status and configuration with your system administrator.")

def is_compatible(blade, config):
    """Check if a blade is compatible with a job config"""
    profile = blade.get('profile', {})
    blade_services = profile.get('service', [])
    blade_envkeys = profile.get('envkey', [])
    
    # Check service
    if config.get('service'):
        if config['service'] not in blade_services:
            return False
    
    # Check envkey
    if config.get('envkey'):
        if not any(ek in blade_envkeys for ek in config['envkey']):
            return False
    
    return True

def main():
    print("Simple Tractor Diagnostics Tool (Python 2.7)")
    print("=" * 50)
    
    if not TRACTOR_AVAILABLE:
        print("\n[FATAL] Tractor API not available. Exiting.")
        return
    
    # Connect to engine
    if not connect_to_engine():
        print("\n[FATAL] Cannot connect to Tractor engine. Exiting.")
        return
    
    # Query blades
    blades = query_blades()
    
    # Query recent jobs
    jobs = query_recent_jobs(limit=5)
    
    # Analyze configurations
    analyze_nuke_configs(blades)
    
    print("\n" + "="*60)
    print("DIAGNOSTICS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
