#!/usr/bin/env python
"""
Enhanced Plugin Loading Fix for Connect.gizmo

Since Connect.gizmo exists at \\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo
and should be loaded by menu.py, this script provides multiple solutions to ensure
proper loading on the render farm.

PROBLEM: Connect.gizmo exists but not loading on render blades
CAUSE: Plugin loading timing or path resolution issues
"""

import nuke
import os

def force_load_connect_gizmo():
    """
    Force load Connect.gizmo explicitly if it's not already available
    """
    print("=" * 60)
    print("ENHANCED CONNECT.GIZMO LOADING")
    print("=" * 60)
    
    # Check if Connect is already available
    try:
        test_node = nuke.nodes.Connect()
        nuke.delete(test_node)
        print("✅ Connect.gizmo already loaded and working")
        return True
    except:
        print("❌ Connect.gizmo not currently available - attempting to load...")
    
    # Try multiple loading methods
    success = False
    
    # Method 1: Direct plugin path addition
    gizmo_paths = [
        r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files",
        r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\gizmos",
        r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke"
    ]
    
    for gizmo_path in gizmo_paths:
        if os.path.exists(gizmo_path):
            print(f"Trying to add plugin path: {gizmo_path}")
            try:
                nuke.pluginAddPath(gizmo_path)
                # Test if Connect is now available
                test_node = nuke.nodes.Connect()
                nuke.delete(test_node)
                print(f"✅ SUCCESS: Connect.gizmo loaded from {gizmo_path}")
                success = True
                break
            except Exception as e:
                print(f"   Failed: {e}")
    
    # Method 2: Direct gizmo file loading
    if not success:
        gizmo_file = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo"
        if os.path.exists(gizmo_file):
            print(f"Trying direct gizmo loading: {gizmo_file}")
            try:
                nuke.pluginLoad(gizmo_file)
                test_node = nuke.nodes.Connect()
                nuke.delete(test_node)
                print("✅ SUCCESS: Connect.gizmo loaded directly")
                success = True
            except Exception as e:
                print(f"   Failed: {e}")
    
    # Method 3: Force reload of all plugins
    if not success:
        print("Attempting plugin reload...")
        try:
            nuke.pluginReload()
            test_node = nuke.nodes.Connect()
            nuke.delete(test_node)
            print("✅ SUCCESS: Connect.gizmo loaded after reload")
            success = True
        except Exception as e:
            print(f"   Failed: {e}")
    
    if success:
        print("\n🎉 Connect.gizmo is now available for rendering")
        return True
    else:
        print("\n❌ Unable to load Connect.gizmo - fallback to replacement needed")
        return False

def enhanced_menu_py_integration():
    """
    Generate enhanced menu.py code to ensure Connect.gizmo loads properly
    """
    
    enhanced_code = '''
# Enhanced Connect.gizmo Loading for Render Farm Compatibility
import nuke
import os

# Original plugin path addition
nuke.pluginAddPath('./nk_files')

# Enhanced loading for Connect.gizmo specifically
def ensure_connect_gizmo_loaded():
    """Ensure Connect.gizmo is properly loaded"""
    try:
        # Test if Connect is available
        test_node = nuke.nodes.Connect()
        nuke.delete(test_node)
        print("Connect.gizmo loaded successfully")
        return True
    except:
        # If not available, try explicit loading
        current_dir = os.path.dirname(__file__)
        gizmo_paths = [
            os.path.join(current_dir, 'nk_files'),
            os.path.join(current_dir, 'gizmos'),
            current_dir
        ]
        
        for path in gizmo_paths:
            connect_file = os.path.join(path, 'Connect.gizmo')
            if os.path.exists(connect_file):
                try:
                    nuke.pluginLoad(connect_file)
                    test_node = nuke.nodes.Connect()
                    nuke.delete(test_node)
                    print(f"Connect.gizmo loaded from {connect_file}")
                    return True
                except:
                    continue
        
        print("WARNING: Connect.gizmo could not be loaded")
        return False

# Call the function to ensure loading
ensure_connect_gizmo_loaded()
'''
    
    return enhanced_code

def create_render_farm_init():
    """
    Create a render-farm specific init file that ensures plugin loading
    """
    
    init_code = '''#!/usr/bin/env python
"""
Render Farm Init Script for Enhanced Plugin Loading
This script ensures all custom plugins load correctly on render blades
"""

import nuke
import os
import sys

def render_farm_plugin_setup():
    """Setup plugins specifically for render farm environment"""
    
    print("Setting up render farm plugins...")
    
    # Base plugin path
    base_path = r"\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke"
    
    # Add all relevant plugin paths
    plugin_subdirs = ['nk_files', 'gizmos', 'python', 'icons', 'images']
    
    for subdir in plugin_subdirs:
        plugin_path = os.path.join(base_path, subdir)
        if os.path.exists(plugin_path):
            nuke.pluginAddPath(plugin_path)
            print(f"Added plugin path: {plugin_path}")
    
    # Specifically ensure Connect.gizmo is loaded
    connect_gizmo = os.path.join(base_path, 'nk_files', 'Connect.gizmo')
    if os.path.exists(connect_gizmo):
        try:
            nuke.pluginLoad(connect_gizmo)
            print("Explicitly loaded Connect.gizmo")
        except Exception as e:
            print(f"Warning: Could not explicitly load Connect.gizmo: {e}")
    
    # Test that Connect is available
    try:
        test_node = nuke.nodes.Connect()
        nuke.delete(test_node)
        print("✅ Connect.gizmo verified working")
    except Exception as e:
        print(f"❌ Connect.gizmo not working: {e}")

# Run setup
render_farm_plugin_setup()
'''
    
    return init_code

def main():
    """
    Main function to demonstrate the enhanced loading
    """
    print("Connect.gizmo Enhanced Loading Solution")
    print("=" * 50)
    
    # Try to load Connect.gizmo
    success = force_load_connect_gizmo()
    
    if success:
        print("\n✅ SOLUTION SUCCESSFUL")
        print("Connect.gizmo is now properly loaded")
        print("\nNext steps:")
        print("1. This loading mechanism should be integrated into menu.py")
        print("2. Test with actual render farm submission")
        print("3. Monitor render logs for success")
    else:
        print("\n❌ ENHANCED LOADING FAILED")
        print("Recommend using emergency replacement scripts")
        print("Issue may require system administrator intervention")
    
    print("\nEnhanced menu.py code:")
    print("-" * 30)
    print(enhanced_menu_py_integration())

if __name__ == "__main__":
    main()
