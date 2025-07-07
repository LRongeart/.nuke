#!/usr/bin/env python
"""
Plugin Loading Diagnostic Script for Tractor Renders

This script tests whether Connect.gizmo and other plugins are loading correctly
on the render farm. Run this as a Tractor job to diagnose plugin loading issues.

Purpose: Determine if Connect.gizmo exists and can be loaded on render blades.
"""

import nuke
import os
import sys

def diagnose_plugin_loading():
    """
    Comprehensive diagnostic of plugin loading on render farm
    """
    
    print("=" * 80)
    print("PLUGIN LOADING DIAGNOSTIC - RENDER FARM")
    print("=" * 80)
    
    # 1. Check environment variables
    print("\n1. ENVIRONMENT VARIABLES:")
    print("-" * 40)
    nuke_path = os.environ.get('NUKE_PATH', 'NOT SET')
    python_path = os.environ.get('PYTHONPATH', 'NOT SET')
    print(f"NUKE_PATH: {nuke_path}")
    print(f"PYTHONPATH: {python_path}")
    
    # 2. Check Nuke plugin paths
    print("\n2. NUKE PLUGIN PATHS:")
    print("-" * 40)
    plugin_paths = nuke.pluginPath()
    for i, path in enumerate(plugin_paths, 1):
        print(f"  {i}. {path}")
        
    # 3. Check if custom init.py loaded
    print("\n3. CUSTOM INIT.PY LOADING:")
    print("-" * 40)
    expected_init = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\init.py"
    init_loaded = any("tls-storage02" in path for path in plugin_paths)
    print(f"Custom init.py loaded: {'YES' if init_loaded else 'NO'}")
    print(f"Expected path: {expected_init}")
    
    # 4. Check for Connect.gizmo file
    print("\n4. CONNECT.GIZMO FILE CHECK:")
    print("-" * 40)
    potential_gizmo_paths = [
        r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo",
        r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\Connect.gizmo",
        r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\gizmos\Connect.gizmo"
    ]
    
    gizmo_found = False
    for gizmo_path in potential_gizmo_paths:
        exists = os.path.exists(gizmo_path)
        print(f"  {gizmo_path}: {'EXISTS' if exists else 'NOT FOUND'}")
        if exists:
            gizmo_found = True
            try:
                size = os.path.getsize(gizmo_path)
                print(f"    Size: {size} bytes")
            except:
                print(f"    Size: Unable to read")
    
    # 5. Test Connect node creation
    print("\n5. CONNECT NODE CREATION TEST:")
    print("-" * 40)
    try:
        # Try to create a Connect node
        connect_node = nuke.nodes.Connect()
        print("✅ SUCCESS: Connect node created successfully")
        print(f"   Node class: {connect_node.Class()}")
        print(f"   Node name: {connect_node.name()}")
        # Clean up
        nuke.delete(connect_node)
    except Exception as e:
        print(f"❌ FAILED: Connect node creation failed")
        print(f"   Error: {e}")
    
    # 6. Check available nodes containing 'Connect'
    print("\n6. AVAILABLE CONNECT-RELATED NODES:")
    print("-" * 40)
    available_nodes = dir(nuke.nodes)
    connect_nodes = [node for node in available_nodes if 'connect' in node.lower()]
    if connect_nodes:
        for node in connect_nodes:
            print(f"  - {node}")
    else:
        print("  No Connect-related nodes found")
    
    # 7. Check all loaded gizmos
    print("\n7. ALL LOADED GIZMOS:")
    print("-" * 40)
    all_nodes = dir(nuke.nodes)
    gizmo_nodes = [node for node in all_nodes if node.endswith('_gizmo') or 'gizmo' in node.lower()]
    if gizmo_nodes:
        for gizmo in gizmo_nodes[:10]:  # Limit to first 10
            print(f"  - {gizmo}")
        if len(gizmo_nodes) > 10:
            print(f"  ... and {len(gizmo_nodes) - 10} more")
    else:
        print("  No gizmos detected in available nodes")
    
    # 8. File system accessibility test
    print("\n8. FILE SYSTEM ACCESSIBILITY:")
    print("-" * 40)
    base_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke"
    try:
        if os.path.exists(base_path):
            print(f"✅ Base path accessible: {base_path}")
            contents = os.listdir(base_path)
            key_folders = [item for item in contents if item in ['nk_files', 'gizmos', 'python']]
            print(f"   Key folders found: {key_folders}")
        else:
            print(f"❌ Base path not accessible: {base_path}")
    except Exception as e:
        print(f"❌ File system error: {e}")
    
    print("\n" + "=" * 80)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 80)
    
    # Summary
    print("\nSUMMARY:")
    if gizmo_found:
        print("✅ Connect.gizmo file found on network storage")
    else:
        print("❌ Connect.gizmo file NOT found")
        
    if init_loaded:
        print("✅ Custom plugin path loaded")
    else:
        print("❌ Custom plugin path NOT loaded")

# Create a simple Nuke script that runs this diagnostic
def create_diagnostic_script():
    """Create a .nk file that runs the diagnostic when rendered"""
    
    # Create a simple constant node
    constant = nuke.nodes.Constant()
    constant['color'].setValue([1, 0, 0, 1])  # Red
    
    # Add Python script node to run diagnostic
    python_node = nuke.nodes.PythonScript()
    python_node.setInput(0, constant)
    
    # Set the Python code
    diagnostic_code = '''
# Run diagnostic when this node is executed
exec(open(r"\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke_DEV\\tractor\\plugin_loading_diagnostic.py").read())
'''
    python_node['python'].setValue(diagnostic_code)
    
    # Create write node for output
    write_node = nuke.nodes.Write()
    write_node.setInput(0, python_node)
    write_node['file'].setValue(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\diagnostic_output.####.exr")
    
    return write_node

if __name__ == "__main__":
    # Run diagnostic if executed as main script
    diagnose_plugin_loading()
