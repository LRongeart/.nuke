#!/usr/bin/env python
"""
Simple Connect.gizmo Loading Test (ASCII only)
Run this in Nuke to test if the permanent fix works
"""

import nuke
import os

def test_connect_gizmo_loading():
    """Test Connect.gizmo loading and report results"""
    
    print("=" * 60)
    print("CONNECT.GIZMO LOADING TEST")
    print("=" * 60)
    
    # Test 1: Check if Connect node is available
    print("\n1. TESTING CONNECT NODE AVAILABILITY:")
    try:
        connect_node = nuke.nodes.Connect()
        print("SUCCESS: Connect node can be created")
        print("   Node class: " + connect_node.Class())
        print("   Node name: " + connect_node.name())
        nuke.delete(connect_node)
        connect_available = True
    except Exception as e:
        print("FAILED: Cannot create Connect node - " + str(e))
        connect_available = False
    
    # Test 2: Check plugin paths
    print("\n2. CHECKING PLUGIN PATHS:")
    plugin_paths = nuke.pluginPath()
    nuke_path_found = False
    for path in plugin_paths:
        if "tls-storage02" in path and "nk_files" in path:
            print("Found nk_files path: " + path)
            nuke_path_found = True
            break
    
    if not nuke_path_found:
        print("nk_files path not found in plugin paths")
    
    # Test 3: Check Connect.gizmo file existence
    print("\n3. CHECKING CONNECT.GIZMO FILE:")
    gizmo_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo"
    if os.path.exists(gizmo_path):
        print("Connect.gizmo file exists: " + gizmo_path)
        try:
            size = os.path.getsize(gizmo_path)
            print("   File size: " + str(size) + " bytes")
        except:
            print("   File size: Unable to read")
    else:
        print("Connect.gizmo file not found: " + gizmo_path)
    
    # Test 4: Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if connect_available:
        print("SUCCESS: Connect.gizmo is working properly!")
        print("   Render farm should handle Connect.gizmo nodes correctly")
        return True
    else:
        print("FAILURE: Connect.gizmo is not working")
        print("   Render jobs with Connect.gizmo will fail")
        print("   Recommend using emergency replacement scripts")
        return False

# Run the test
if __name__ == "__main__":
    test_connect_gizmo_loading()
