#!/usr/bin/env python
"""
Quick Tractor Job Test
======================

This script quickly tests if a specific job configuration will be picked up by blades.
Use this to test your exact job parameters before submitting through Nuke.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from tractor_diagnostics import TractorDiagnostics
except ImportError:
    print("[ERROR] Could not import tractor_diagnostics. Make sure it's in the same directory.")
    sys.exit(1)

def test_job_config(service=None, envkey=None, crews=None, owner="TrackerUser", priority=500):
    """Test a specific job configuration"""
    
    # Convert single values to lists where appropriate
    if envkey and isinstance(envkey, str):
        envkey = [envkey]
    if crews and isinstance(crews, str):
        crews = [crews]
    
    config = {
        'name': f'Custom Test - {service or "No Service"}',
        'service': service,
        'envkey': envkey or [],
        'crews': crews or [],
        'owner': owner,
        'priority': priority
    }
    
    print(f"Testing job configuration:")
    print(f"  Service: {config['service']}")
    print(f"  Envkey: {config['envkey']}")
    print(f"  Crews: {config['crews']}")
    print(f"  Owner: {config['owner']}")
    print(f"  Priority: {config['priority']}")
    
    diag = TractorDiagnostics()
    
    if not diag.connect_to_engine():
        print("[ERROR] Cannot connect to Tractor engine")
        return False
    
    diag.query_all_blades()
    compatible, incompatible = diag.analyze_job_blade_compatibility(config)
    
    return len(compatible) > 0

def interactive_test():
    """Interactive mode for testing different configurations"""
    print("Interactive Tractor Job Configuration Tester")
    print("=" * 50)
    
    while True:
        print("\nEnter job configuration (press Enter for default/none):")
        
        service = input("Service (e.g., NukeXRender, NukeRender): ").strip()
        if not service:
            service = None
            
        envkey = input("Envkey (e.g., rez): ").strip()
        if not envkey:
            envkey = None
            
        crews = input("Crews (comma-separated): ").strip()
        if crews:
            crews = [c.strip() for c in crews.split(",")]
        else:
            crews = None
            
        owner = input("Owner (default: TrackerUser): ").strip()
        if not owner:
            owner = "TrackerUser"
            
        try:
            priority = int(input("Priority (default: 500): ").strip() or "500")
        except ValueError:
            priority = 500
        
        print("\n" + "-" * 50)
        will_be_picked_up = test_job_config(service, envkey, crews, owner, priority)
        
        if will_be_picked_up:
            print("\n✅ SUCCESS: This job configuration should be picked up by blades!")
        else:
            print("\n❌ FAILURE: This job configuration will NOT be picked up by any blades!")
        
        print("\n" + "-" * 50)
        again = input("Test another configuration? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        service = sys.argv[1] if len(sys.argv) > 1 else None
        envkey = sys.argv[2] if len(sys.argv) > 2 else None
        crews = sys.argv[3] if len(sys.argv) > 3 else None
        
        print("Command line test mode:")
        success = test_job_config(service, envkey, crews)
        sys.exit(0 if success else 1)
    else:
        # Interactive mode
        interactive_test()
