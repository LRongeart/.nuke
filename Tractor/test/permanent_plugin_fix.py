#!/usr/bin/env python
"""
Enhanced menu.py Integration for Permanent Connect.gizmo Fix

This script creates an enhanced version of the plugin loading mechanism
that should be integrated into the main menu.py file to ensure Connect.gizmo
loads properly on all render farm nodes.
"""

def create_enhanced_menu_integration():
    """
    Create enhanced menu.py code for permanent Connect.gizmo loading fix
    """
    
    enhanced_menu_code = '''
#*****************************************************************
# ENHANCED CONNECT.GIZMO LOADING FOR RENDER FARM COMPATIBILITY
# Added: June 26, 2025 - Permanent fix for Connect.gizmo loading issues
#*****************************************************************

import nuke
import os
import sys

# Original plugin path additions (keep existing)
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./python')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./images')
nuke.pluginAddPath('./nk_files')
nuke.pluginAddPath('./performanceTimers')

# ENHANCED CONNECT.GIZMO LOADING MECHANISM
def ensure_connect_gizmo_loaded():
    """
    Enhanced Connect.gizmo loading with multiple fallback methods
    Specifically designed to work on render farm environments
    """
    
    def test_connect_availability():
        """Test if Connect node can be created"""
        try:
            test_node = nuke.nodes.Connect()
            nuke.delete(test_node)
            return True
        except:
            return False
    
    # Quick test - if Connect is already working, we're done
    if test_connect_availability():
        print("[PLUGIN] Connect.gizmo already loaded and working")
        return True
    
    print("[PLUGIN] Connect.gizmo not available - attempting enhanced loading...")
    
    # Get the directory where this menu.py is located
    current_dir = os.path.dirname(__file__)
    
    # Method 1: Explicit path addition with verification
    gizmo_search_paths = [
        os.path.join(current_dir, 'nk_files'),
        os.path.join(current_dir, 'gizmos'),
        current_dir,
        # Absolute paths as fallback
        r'\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\nk_files',
        r'\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\gizmos',
        r'\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke'
    ]
    
    for search_path in gizmo_search_paths:
        if os.path.exists(search_path):
            print(f"[PLUGIN] Checking path: {search_path}")
            
            # Add the path to plugin search
            try:
                nuke.pluginAddPath(search_path)
            except:
                pass
            
            # Look for Connect.gizmo file specifically
            connect_gizmo_file = os.path.join(search_path, 'Connect.gizmo')
            if os.path.exists(connect_gizmo_file):
                print(f"[PLUGIN] Found Connect.gizmo at: {connect_gizmo_file}")
                
                # Method 2: Direct file loading
                try:
                    nuke.pluginLoad(connect_gizmo_file)
                    print(f"[PLUGIN] Loaded Connect.gizmo from {connect_gizmo_file}")
                    
                    if test_connect_availability():
                        print("[PLUGIN] ✅ Connect.gizmo successfully loaded!")
                        return True
                        
                except Exception as e:
                    print(f"[PLUGIN] Direct load failed: {e}")
    
    # Method 3: Force plugin reload
    print("[PLUGIN] Attempting plugin system reload...")
    try:
        nuke.pluginReload()
        if test_connect_availability():
            print("[PLUGIN] ✅ Connect.gizmo loaded after plugin reload!")
            return True
    except Exception as e:
        print(f"[PLUGIN] Plugin reload failed: {e}")
    
    # Method 4: Manual gizmo registration (last resort)
    print("[PLUGIN] Attempting manual gizmo registration...")
    try:
        # Try to manually register the gizmo
        gizmo_file = r'\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\nk_files\\Connect.gizmo'
        if os.path.exists(gizmo_file):
            # Read and execute the gizmo file
            with open(gizmo_file, 'r') as f:
                gizmo_content = f.read()
            
            # This is a more advanced approach - execute the gizmo definition
            exec(gizmo_content, globals())
            
            if test_connect_availability():
                print("[PLUGIN] ✅ Connect.gizmo manually registered!")
                return True
                
    except Exception as e:
        print(f"[PLUGIN] Manual registration failed: {e}")
    
    print("[PLUGIN] ❌ Connect.gizmo could not be loaded - render farm may need attention")
    print("[PLUGIN] Recommendation: Use Connect.gizmo replacement tools for immediate renders")
    return False

# EXECUTE ENHANCED LOADING
try:
    connect_loaded = ensure_connect_gizmo_loaded()
    if connect_loaded:
        print("[PLUGIN] Connect.gizmo is ready for use")
    else:
        print("[PLUGIN] Connect.gizmo loading failed - fallback solutions available")
except Exception as e:
    print(f"[PLUGIN] Enhanced loading error: {e}")

#*****************************************************************
# END OF ENHANCED CONNECT.GIZMO LOADING
#*****************************************************************
'''
    
    return enhanced_menu_code

def create_permanent_init_fix():
    """
    Create a permanent init.py addition for render farm compatibility
    """
    
    init_addition = '''
#*****************************************************************
# RENDER FARM PLUGIN COMPATIBILITY - Added June 26, 2025
#*****************************************************************

def setup_render_farm_plugins():
    """Setup plugins specifically for render farm compatibility"""
    
    import nuke
    import os
    
    print("[RENDER FARM] Setting up enhanced plugin loading...")
    
    # Ensure all critical paths are available
    base_plugin_path = r"\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke"
    
    critical_paths = [
        os.path.join(base_plugin_path, 'nk_files'),
        os.path.join(base_plugin_path, 'gizmos'),  
        os.path.join(base_plugin_path, 'python'),
        base_plugin_path
    ]
    
    # Add each path and verify accessibility
    for path in critical_paths:
        if os.path.exists(path):
            nuke.pluginAddPath(path)
            print(f"[RENDER FARM] Added plugin path: {path}")
        else:
            print(f"[RENDER FARM] WARNING: Path not accessible: {path}")
    
    # Specific Connect.gizmo handling
    connect_gizmo = os.path.join(base_plugin_path, 'nk_files', 'Connect.gizmo')
    if os.path.exists(connect_gizmo):
        try:
            nuke.pluginLoad(connect_gizmo)
            print("[RENDER FARM] Connect.gizmo explicitly loaded")
            
            # Verify it works
            test_node = nuke.nodes.Connect()
            nuke.delete(test_node)
            print("[RENDER FARM] ✅ Connect.gizmo verified working")
            
        except Exception as e:
            print(f"[RENDER FARM] ❌ Connect.gizmo load failed: {e}")
    else:
        print(f"[RENDER FARM] ❌ Connect.gizmo not found at: {connect_gizmo}")

# Execute render farm setup
try:
    setup_render_farm_plugins()
except Exception as e:
    print(f"[RENDER FARM] Setup failed: {e}")

#*****************************************************************
# END OF RENDER FARM COMPATIBILITY
#*****************************************************************
'''
    
    return init_addition

def generate_implementation_guide():
    """Generate step-by-step implementation guide"""
    
    guide = """
# PERMANENT CONNECT.GIZMO FIX - IMPLEMENTATION GUIDE

## Overview
This permanent solution enhances the existing menu.py and init.py files to ensure
Connect.gizmo loads properly on all render farm nodes.

## Implementation Steps

### Step 1: Backup Current Files
```bash
# Backup the original files
copy "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py" "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py.backup"
copy "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\init.py" "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\init.py.backup"
```

### Step 2: Add Enhanced Loading to menu.py
Add the enhanced Connect.gizmo loading code to the existing menu.py file.
This code provides multiple fallback methods for loading Connect.gizmo.

### Step 3: Add Render Farm Setup to init.py  
Add the render farm compatibility code to the existing init.py file.
This ensures proper plugin paths and explicit Connect.gizmo loading.

### Step 4: Test Implementation
1. Submit a diagnostic job to verify loading works
2. Test with an actual render job using Connect.gizmo
3. Monitor render logs for success

### Step 5: Rollback Plan (if needed)
If any issues occur, restore the original files:
```bash
copy "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py.backup" "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py"
copy "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\init.py.backup" "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\init.py"
```

## Expected Results
- Connect.gizmo loads properly on all render farm nodes
- No more "unknown command" errors for Connect.gizmo
- Existing functionality preserved
- Enhanced error reporting for troubleshooting

## Monitoring
After implementation, monitor render logs for:
- "[PLUGIN] Connect.gizmo successfully loaded!" messages
- Absence of "Connect.gizmo: unknown command" errors
- Successful completion of renders using Connect.gizmo nodes
"""
    
    return guide

def main():
    """Main function to create all permanent solution files"""
    
    print("=" * 60)
    print("CREATING PERMANENT CONNECT.GIZMO SOLUTION")
    print("=" * 60)
    
    # Create enhanced menu.py code
    enhanced_menu = create_enhanced_menu_integration()
    
    # Create init.py addition
    init_addition = create_permanent_init_fix()
    
    # Create implementation guide
    implementation_guide = generate_implementation_guide()
    
    print("✅ Enhanced menu.py code created")
    print("✅ Init.py addition created") 
    print("✅ Implementation guide created")
    
    print("\nNext steps:")
    print("1. Review the generated code")
    print("2. Backup original menu.py and init.py")
    print("3. Integrate enhanced code into existing files")
    print("4. Test with diagnostic job")
    print("5. Deploy to production")
    
    return enhanced_menu, init_addition, implementation_guide

if __name__ == "__main__":
    main()
