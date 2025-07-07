# Test script to help debug blade matching issues
# Run this from within Nuke to test different service/envkey combinations

import sys
import os

# Add the tractor directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from submit_to_tractor_ui import get_blade_info, spool_job_via_bridge
from tractor.base.api.author import Job, Task

def test_service_combinations():
    """Test different service/envkey combinations to see what works"""
    
    # Get available blades first
    print("=== Available Blades ===")
    blade_info = get_blade_info()
    if blade_info:
        for blade in blade_info:
            print(f"Blade: {blade['name']}")
            print(f"  Services: {blade['services']}")
            print(f"  Envkeys: {blade['envkeys']}")
            print(f"  Crews: {blade['crews']}")
            print()
    else:
        print("No blade info available")
        return
    
    # Test combinations based on what we found
    test_combinations = []
    
    # Extract unique services and envkeys from blades
    all_services = set()
    all_envkeys = set()
    for blade in blade_info:
        all_services.update(blade['services'])
        all_envkeys.update(blade['envkeys'])
    
    print(f"Found services: {list(all_services)}")
    print(f"Found envkeys: {list(all_envkeys)}")
    
    # Create test combinations
    for service in all_services:
        if 'nuke' in str(service).lower():
            for envkey in all_envkeys:
                if 'nuke' in str(envkey).lower():
                    test_combinations.append((service, envkey))
    
    print(f"\n=== Testing {len(test_combinations)} combinations ===")
    
    for service, envkey in test_combinations:
        print(f"\nTesting: service={service}, envkey={envkey}")
        
        # Create a simple test job
        job = Job()
        job.title = f"[TEST] Blade matching test - {service}/{envkey}"
        job.service = service
        job.envkey = [envkey]
        job.crews = ['3D4']
        job.tier = "windows"
        job.minslots = 1
        job.maxslots = 1
        job.maxactive = 1
        job.priority = 1000  # Low priority for testing
        
        # Create a simple test task
        test_task = Task(title="Test Task", argv=["echo", "test"])
        job.addChild(test_task)
        
        try:
            result = spool_job_via_bridge(job.asTcl())
            print(f"  SUCCESS: Job submitted with ID {result}")
        except Exception as e:
            print(f"  FAILED: {e}")

if __name__ == "__main__":
    test_service_combinations()
