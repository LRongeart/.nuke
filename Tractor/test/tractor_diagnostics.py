#!/usr/bin/env python
"""
Tractor Diagnostics Tool
========================

This tool helps diagnose why Tractor jobs are not being picked up by blades.
It analyzes blade capabilities, job requirements, and provides detailed 
compatibility reports.

Usage:
    python tractor_diagnostics.py
"""

import os
import sys
import json
from pprint import pprint

# Add the current directory to sys.path to import our modules
sys.path.insert(0, os.path.dirname(__file__))

# Try to add local Tractor API paths
script_dir = os.path.dirname(__file__)
tractor_paths = [
    script_dir,  # Current directory has tractor modules
    os.path.join(script_dir, 'python2.7_portable', 'App', 'Python', 'Lib', 'site-packages'),
    os.path.join(script_dir, '..', '..', '..', 'Tractor-2.0', 'lib', 'python2.7', 'site-packages'),
]

for path in tractor_paths:
    if os.path.exists(path):
        sys.path.insert(0, path)
        print(f"[DEBUG] Added to Python path: {path}")

print(f"[DEBUG] Python path includes: {sys.path[:3]}...")  # Show first few paths

try:
    # Try different import paths for Tractor API
    try:
        import tractor.api.query as tq
        from tractor.api.author import Job, Task, Command
        print("[DEBUG] Successfully imported tractor.api modules")
    except ImportError:
        # Try importing from current directory structure
        import api.query as tq
        from api.author import Job, Task, Command
        print("[DEBUG] Successfully imported api modules from local directory")
    
    TRACTOR_AVAILABLE = True
    print("[SUCCESS] Tractor API is available")
except ImportError as e:
    print(f"[ERROR] Tractor API not available: {e}")
    print("[ERROR] Checked paths:")
    for path in tractor_paths:
        exists = "✓" if os.path.exists(path) else "✗"
        print(f"  {exists} {path}")
    print("[ERROR] Make sure TRACTOR_ENGINE is set and Tractor is properly installed.")
    TRACTOR_AVAILABLE = False

# Import our configuration
SIMTRACKER = {
    "host": "simtracker", 
    "port": 80,
    "user": "TrackerUser",
    "password": "TrackerUser"
}

class TractorDiagnostics:
    def __init__(self):
        self.blades = []
        self.jobs = []
        self.engine_connected = False
        
    def connect_to_engine(self):
        """Connect to Tractor engine"""
        try:
            print(f"[INFO] Connecting to Tractor engine at {SIMTRACKER['host']}:{SIMTRACKER['port']}")
            tq.setEngineClientParam(
                hostname=SIMTRACKER["host"],
                port=SIMTRACKER["port"],
                user=SIMTRACKER["user"],
                password=SIMTRACKER["password"]
            )
            
            # Test connection by querying engine status
            jobs = tq.jobs(limit=1)
            self.engine_connected = True
            print("[SUCCESS] Connected to Tractor engine successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to connect to Tractor engine: {e}")
            return False
    
    def query_all_blades(self):
        """Query all available blades and their capabilities"""
        if not self.engine_connected:
            return []
            
        try:
            print("\n" + "="*60)
            print("BLADE ANALYSIS")
            print("="*60)
            
            blades = tq.blades()
            print(f"[INFO] Found {len(blades) if blades else 0} total blades")
            
            if not blades:
                print("[WARNING] No blades found!")
                return []
            
            self.blades = []
            active_count = 0
            
            for i, blade in enumerate(blades):
                blade_name = blade.get('name', f'blade_{i}')
                nimby = blade.get('nimby', 'unknown')
                profile = blade.get('profile', {})
                
                blade_info = {
                    'name': blade_name,
                    'nimby': nimby,
                    'active': nimby == 'off',
                    'services': profile.get('service', []),
                    'envkeys': profile.get('envkey', []),
                    'crews': profile.get('crews', []),
                    'capacity': blade.get('capacity', 1),
                    'availcapacity': blade.get('availcapacity', 0),
                    'numslots': blade.get('numslots', 1),
                    'availslots': blade.get('availslots', 0),
                    'boottime': blade.get('boottime', 'unknown'),
                    'ipaddr': blade.get('ipaddr', 'unknown'),
                    'profile': profile
                }
                
                self.blades.append(blade_info)
                
                if nimby == 'off':
                    active_count += 1
                    
                print(f"\nBlade: {blade_name}")
                print(f"  Status: {'ACTIVE' if nimby == 'off' else 'NIMBY'}")
                print(f"  Services: {blade_info['services']}")
                print(f"  Envkeys: {blade_info['envkeys']}")
                print(f"  Crews: {blade_info['crews']}")
                print(f"  Capacity: {blade_info['capacity']} (available: {blade_info['availcapacity']})")
                print(f"  Slots: {blade_info['numslots']} (available: {blade_info['availslots']})")
                print(f"  IP: {blade_info['ipaddr']}")
                
            print(f"\n[SUMMARY] {active_count}/{len(blades)} blades are active (nimby=off)")
            return self.blades
            
        except Exception as e:
            print(f"[ERROR] Failed to query blades: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def query_recent_jobs(self, limit=10):
        """Query recent jobs to see what's working"""
        if not self.engine_connected:
            return []
            
        try:
            print("\n" + "="*60)
            print("RECENT JOBS ANALYSIS")
            print("="*60)
            
            jobs = tq.jobs(limit=limit)
            print(f"[INFO] Found {len(jobs) if jobs else 0} recent jobs")
            
            if not jobs:
                print("[WARNING] No recent jobs found!")
                return []
            
            self.jobs = []
            
            for job in jobs:
                job_info = {
                    'jid': job.get('jid', 'unknown'),
                    'title': job.get('title', 'untitled'),
                    'owner': job.get('owner', 'unknown'),
                    'state': job.get('state', 'unknown'),
                    'service': job.get('service', 'unknown'),
                    'envkey': job.get('envkey', []),
                    'crews': job.get('crews', []),
                    'priority': job.get('priority', 0),
                    'maxactive': job.get('maxactive', 1),
                    'serialsubtasks': job.get('serialsubtasks', 0),
                    'spooltime': job.get('spooltime', 'unknown'),
                    'starttime': job.get('starttime', 'unknown'),
                    'stoptime': job.get('stoptime', 'unknown')
                }
                
                self.jobs.append(job_info)
                
                print(f"\nJob {job_info['jid']}: {job_info['title']}")
                print(f"  Owner: {job_info['owner']}")
                print(f"  State: {job_info['state']}")
                print(f"  Service: {job_info['service']}")
                print(f"  Envkey: {job_info['envkey']}")
                print(f"  Crews: {job_info['crews']}")
                print(f"  Priority: {job_info['priority']}")
                print(f"  MaxActive: {job_info['maxactive']}")
                print(f"  Serial: {job_info['serialsubtasks']}")
                
            return self.jobs
            
        except Exception as e:
            print(f"[ERROR] Failed to query jobs: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def analyze_job_blade_compatibility(self, job_config):
        """Analyze why a job configuration might not be picked up by blades"""
        print("\n" + "="*60)
        print("JOB-BLADE COMPATIBILITY ANALYSIS")
        print("="*60)
        
        print(f"Job Configuration:")
        print(f"  Service: {job_config.get('service', 'None')}")
        print(f"  Envkey: {job_config.get('envkey', 'None')}")
        print(f"  Crews: {job_config.get('crews', 'None')}")
        print(f"  Owner: {job_config.get('owner', 'None')}")
        print(f"  Priority: {job_config.get('priority', 0)}")
        
        if not self.blades:
            print("[ERROR] No blade data available. Run query_all_blades() first.")
            return
        
        compatible_blades = []
        incompatible_blades = []
        
        for blade in self.blades:
            if not blade['active']:
                incompatible_blades.append((blade, ["Blade is not active (nimby=on)"]))
                continue
                
            issues = []
            
            # Check service compatibility
            job_service = job_config.get('service')
            if job_service and job_service not in blade['services']:
                if blade['services']:
                    issues.append(f"Service mismatch: job needs '{job_service}', blade has {blade['services']}")
                else:
                    issues.append(f"Service mismatch: job needs '{job_service}', blade has no services")
            
            # Check envkey compatibility
            job_envkey = job_config.get('envkey', [])
            if isinstance(job_envkey, str):
                job_envkey = [job_envkey]
            if job_envkey:
                blade_envkeys = blade['envkeys']
                if not any(envkey in blade_envkeys for envkey in job_envkey):
                    issues.append(f"Envkey mismatch: job needs {job_envkey}, blade has {blade_envkeys}")
            
            # Check crew compatibility
            job_crews = job_config.get('crews', [])
            if isinstance(job_crews, str):
                job_crews = [job_crews]
            if job_crews:
                blade_crews = blade['crews']
                if not any(crew in blade_crews for crew in job_crews):
                    issues.append(f"Crew mismatch: job needs {job_crews}, blade has {blade_crews}")
            
            # Check capacity
            if blade['availcapacity'] <= 0:
                issues.append(f"No available capacity: {blade['availcapacity']}/{blade['capacity']}")
            
            if blade['availslots'] <= 0:
                issues.append(f"No available slots: {blade['availslots']}/{blade['numslots']}")
            
            if issues:
                incompatible_blades.append((blade, issues))
            else:
                compatible_blades.append(blade)
        
        print(f"\n[RESULTS]")
        print(f"Compatible blades: {len(compatible_blades)}")
        print(f"Incompatible blades: {len(incompatible_blades)}")
        
        if compatible_blades:
            print(f"\n✅ COMPATIBLE BLADES:")
            for blade in compatible_blades:
                print(f"  - {blade['name']} (capacity: {blade['availcapacity']}/{blade['capacity']})")
        
        if incompatible_blades:
            print(f"\n❌ INCOMPATIBLE BLADES:")
            for blade, issues in incompatible_blades:
                print(f"  - {blade['name']}:")
                for issue in issues:
                    print(f"    * {issue}")
        
        # Provide recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if not compatible_blades:
            print("  - No blades can pick up this job configuration!")
            
            # Analyze common issues
            service_issues = sum(1 for _, issues in incompatible_blades if any("Service mismatch" in issue for issue in issues))
            envkey_issues = sum(1 for _, issues in incompatible_blades if any("Envkey mismatch" in issue for issue in issues))
            crew_issues = sum(1 for _, issues in incompatible_blades if any("Crew mismatch" in issue for issue in issues))
            capacity_issues = sum(1 for _, issues in incompatible_blades if any("capacity" in issue for issue in issues))
            
            if service_issues > 0:
                available_services = set()
                for blade in self.blades:
                    if blade['active']:
                        available_services.update(blade['services'])
                print(f"  - Service issues ({service_issues} blades): try using one of {list(available_services)}")
            
            if envkey_issues > 0:
                available_envkeys = set()
                for blade in self.blades:
                    if blade['active']:
                        available_envkeys.update(blade['envkeys'])
                print(f"  - Envkey issues ({envkey_issues} blades): try using one of {list(available_envkeys)}")
            
            if crew_issues > 0:
                available_crews = set()
                for blade in self.blades:
                    if blade['active']:
                        available_crews.update(blade['crews'])
                print(f"  - Crew issues ({crew_issues} blades): try using one of {list(available_crews)}")
            
            if capacity_issues > 0:
                print(f"  - Capacity issues ({capacity_issues} blades): wait for blades to finish current tasks")
        
        else:
            print(f"  - Job should be picked up by {len(compatible_blades)} compatible blade(s)")
            print(f"  - If job is still not picked up, check:")
            print(f"    * Job priority (higher priority jobs get picked up first)")
            print(f"    * Job state (should be 'ready' not 'blocked' or 'paused')")
            print(f"    * Tractor engine logs for additional errors")
        
        return compatible_blades, incompatible_blades
    
    def test_nuke_job_config(self):
        """Test a typical Nuke job configuration"""
        print("\n" + "="*60)
        print("TESTING NUKE JOB CONFIGURATION")
        print("="*60)
        
        # Test different service configurations
        test_configs = [
            {
                'name': 'NukeXRender Service',
                'service': 'NukeXRender',
                'envkey': ['rez'],
                'crews': [],
                'owner': 'TrackerUser',
                'priority': 500
            },
            {
                'name': 'NukeRender Service',
                'service': 'NukeRender', 
                'envkey': ['rez'],
                'crews': [],
                'owner': 'TrackerUser',
                'priority': 500
            },
            {
                'name': 'No Service (Default)',
                'service': None,
                'envkey': [],
                'crews': [],
                'owner': 'TrackerUser',
                'priority': 500
            },
            {
                'name': 'Generic Service',
                'service': 'generic',
                'envkey': [],
                'crews': [],
                'owner': 'TrackerUser',
                'priority': 500
            }
        ]
        
        results = {}
        for config in test_configs:
            print(f"\n🧪 Testing: {config['name']}")
            compatible, incompatible = self.analyze_job_blade_compatibility(config)
            results[config['name']] = {
                'compatible_count': len(compatible),
                'incompatible_count': len(incompatible),
                'config': config
            }
        
        # Summary
        print(f"\n📊 TEST SUMMARY:")
        best_config = None
        best_count = 0
        
        for name, result in results.items():
            count = result['compatible_count']
            print(f"  {name}: {count} compatible blade(s)")
            if count > best_count:
                best_count = count
                best_config = result['config']
        
        if best_config:
            print(f"\n🏆 RECOMMENDED CONFIGURATION:")
            for key, value in best_config.items():
                if key != 'name':
                    print(f"  {key}: {value}")
        else:
            print(f"\n❌ NO WORKING CONFIGURATION FOUND")
            print(f"  Check that blades are active and properly configured")
        
        return results
    
    def generate_test_job_tcl(self, config):
        """Generate a test job TCL string for debugging"""
        job_tcl = f'''
Job {{
    title "Test Job - {config.get('name', 'Unknown')}"
    priority {config.get('priority', 500)}
    crews {{"{'" "'.join(config.get('crews', []))}"}}
    service "{config.get('service', '')}"
    envkey {{"{'" "'.join(config.get('envkey', []))}"}}
    maxactive {config.get('maxactive', 1)}
    
    Task {{
        title "Test Task"
        id "test_task"
        
        Command {{
            argv {{"echo" "Test command from Tractor diagnostics"}}
        }}
    }}
}}
'''
        return job_tcl.strip()

def main():
    print("Tractor Diagnostics Tool")
    print("========================")
    
    if not TRACTOR_AVAILABLE:
        print("\n[FATAL] Tractor API not available. Exiting.")
        return
    
    diag = TractorDiagnostics()
    
    # Connect to engine
    if not diag.connect_to_engine():
        print("\n[FATAL] Cannot connect to Tractor engine. Exiting.")
        return
    
    # Query blades
    blades = diag.query_all_blades()
    if not blades:
        print("\n[WARNING] No blades found. Job pickup analysis will be limited.")
    
    # Query recent jobs  
    jobs = diag.query_recent_jobs(limit=5)
    
    # Test Nuke job configurations
    diag.test_nuke_job_config()
    
    print(f"\n" + "="*60)
    print("DIAGNOSTICS COMPLETE")
    print("="*60)
    print(f"Summary:")
    print(f"  - Connected to Tractor engine: ✅")
    print(f"  - Total blades found: {len(blades)}")
    print(f"  - Active blades: {sum(1 for b in blades if b['active'])}")
    print(f"  - Recent jobs: {len(jobs)}")
    print(f"\nFor detailed analysis, review the output above.")
    print(f"Use the recommended configuration in your Nuke submission script.")

if __name__ == "__main__":
    main()
