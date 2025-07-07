#!/usr/bin/env python
"""
Permanent Connect.gizmo Fix - Direct Implementation

This script directly implements the permanent solution by creating enhanced
versions of menu.py and init.py that ensure Connect.gizmo loads properly.
"""

import os
import shutil

def backup_original_files():
    """Create backups of original files before modification"""
    
    base_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke"
    
    files_to_backup = [
        "menu.py",
        "init.py"
    ]
    
    print("Creating backups of original files...")
    
    for filename in files_to_backup:
        original_path = os.path.join(base_path, filename)
        backup_path = os.path.join(base_path, f"{filename}.backup_{os.getpid()}")
        
        if os.path.exists(original_path):
            try:
                shutil.copy2(original_path, backup_path)
                print(f"✅ Backed up: {filename} → {os.path.basename(backup_path)}")
            except Exception as e:
                print(f"❌ Failed to backup {filename}: {e}")
                return False
        else:
            print(f"⚠ File not found: {original_path}")
    
    return True

def create_enhanced_menu_py():
    """Create enhanced menu.py with Connect.gizmo loading fix"""
    
    # Read the original menu.py
    original_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\menu.py"
    
    try:
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Failed to read original menu.py: {e}")
        return False
    
    # Find the location to insert our enhancement (after pluginAddPath calls)
    insert_point = original_content.find("nuke.pluginAddPath('./performanceTimers')")
    
    if insert_point == -1:
        # Fallback: insert after nk_files
        insert_point = original_content.find("nuke.pluginAddPath('./nk_files')")
        if insert_point == -1:
            print("Could not find insertion point in menu.py")
            return False
    
    # Find the end of the line
    insert_point = original_content.find('\n', insert_point) + 1
    
    # Enhanced Connect.gizmo loading code
    enhancement_code = '''
#*****************************************************************
# ENHANCED CONNECT.GIZMO LOADING - Added June 26, 2025
# Permanent fix for Connect.gizmo loading issues on render farm
#*****************************************************************

def ensure_connect_gizmo_loaded():
    """Enhanced Connect.gizmo loading with multiple fallback methods"""
    
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
        print("[CONNECT] Connect.gizmo already loaded and working")
        return True
    
    print("[CONNECT] Connect.gizmo not available - attempting enhanced loading...")
    
    # Get the directory where this menu.py is located
    current_dir = os.path.dirname(__file__)
    
    # Method 1: Explicit path verification and loading
    gizmo_search_paths = [
        os.path.join(current_dir, 'nk_files'),
        os.path.join(current_dir, 'gizmos'),
        current_dir
    ]
    
    for search_path in gizmo_search_paths:
        if os.path.exists(search_path):
            print(f"[CONNECT] Checking path: {search_path}")
            
            # Ensure the path is in plugin paths
            try:
                nuke.pluginAddPath(search_path)
            except:
                pass
            
            # Look for Connect.gizmo file specifically
            connect_gizmo_file = os.path.join(search_path, 'Connect.gizmo')
            if os.path.exists(connect_gizmo_file):
                print(f"[CONNECT] Found Connect.gizmo at: {connect_gizmo_file}")
                
                # Method 2: Direct file loading
                try:
                    nuke.pluginLoad(connect_gizmo_file)
                    print(f"[CONNECT] Loaded Connect.gizmo from {connect_gizmo_file}")
                    
                    if test_connect_availability():
                        print("[CONNECT] ✅ Connect.gizmo successfully loaded!")
                        return True
                        
                except Exception as e:
                    print(f"[CONNECT] Direct load failed: {e}")
    
    # Method 3: Force plugin reload
    print("[CONNECT] Attempting plugin system reload...")
    try:
        nuke.pluginReload()
        if test_connect_availability():
            print("[CONNECT] ✅ Connect.gizmo loaded after plugin reload!")
            return True
    except Exception as e:
        print(f"[CONNECT] Plugin reload failed: {e}")
    
    print("[CONNECT] ❌ Connect.gizmo could not be loaded")
    print("[CONNECT] Render jobs using Connect.gizmo may fail")
    print("[CONNECT] Recommendation: Use Connect.gizmo replacement tools")
    return False

# Execute enhanced loading
try:
    connect_loaded = ensure_connect_gizmo_loaded()
    if connect_loaded:
        print("[CONNECT] Connect.gizmo is ready for use on render farm")
except Exception as e:
    print(f"[CONNECT] Enhanced loading error: {e}")

#*****************************************************************
# END OF ENHANCED CONNECT.GIZMO LOADING
#*****************************************************************

'''
    
    # Insert the enhancement code
    enhanced_content = (
        original_content[:insert_point] + 
        enhancement_code + 
        original_content[insert_point:]
    )
    
    # Write the enhanced version
    enhanced_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\enhanced_menu.py"
    
    try:
        with open(enhanced_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        print(f"✅ Enhanced menu.py created at: {enhanced_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to write enhanced menu.py: {e}")
        return False

def create_render_farm_test_script():
    """Create a test script to verify Connect.gizmo loading works"""
    
    test_script = '''#!/usr/bin/env python
"""
Test script to verify Connect.gizmo loading on render farm
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
    print("\\n1. TESTING CONNECT NODE AVAILABILITY:")
    try:
        connect_node = nuke.nodes.Connect()
        print("✅ SUCCESS: Connect node can be created")
        print(f"   Node class: {connect_node.Class()}")
        print(f"   Node name: {connect_node.name()}")
        nuke.delete(connect_node)
        connect_available = True
    except Exception as e:
        print(f"❌ FAILED: Cannot create Connect node - {e}")
        connect_available = False
    
    # Test 2: Check plugin paths
    print("\\n2. CHECKING PLUGIN PATHS:")
    plugin_paths = nuke.pluginPath()
    nuke_path_found = False
    for path in plugin_paths:
        if "tls-storage02" in path and "nk_files" in path:
            print(f"✅ Found nk_files path: {path}")
            nuke_path_found = True
            break
    
    if not nuke_path_found:
        print("❌ nk_files path not found in plugin paths")
    
    # Test 3: Check Connect.gizmo file existence
    print("\\n3. CHECKING CONNECT.GIZMO FILE:")
    gizmo_path = r"\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\nk_files\\Connect.gizmo"
    if os.path.exists(gizmo_path):
        print(f"✅ Connect.gizmo file exists: {gizmo_path}")
        try:
            size = os.path.getsize(gizmo_path)
            print(f"   File size: {size} bytes")
        except:
            print("   File size: Unable to read")
    else:
        print(f"❌ Connect.gizmo file not found: {gizmo_path}")
    
    # Test 4: Summary
    print("\\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if connect_available:
        print("🎉 SUCCESS: Connect.gizmo is working properly!")
        print("   Render farm should handle Connect.gizmo nodes correctly")
        return True
    else:
        print("❌ FAILURE: Connect.gizmo is not working")
        print("   Render jobs with Connect.gizmo will fail")
        print("   Recommend using emergency replacement scripts")
        return False

if __name__ == "__main__":
    test_connect_gizmo_loading()
'''
    
    test_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\test_connect_loading.py"
    
    try:
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_script)
        print(f"✅ Test script created at: {test_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create test script: {e}")
        return False

def create_deployment_guide():
    """Create deployment guide for the permanent solution"""
    
    guide = '''# PERMANENT CONNECT.GIZMO FIX - DEPLOYMENT GUIDE

## Quick Deployment Steps

### Step 1: Review Enhanced menu.py
```
enhanced_menu.py has been created with the permanent fix.
Review this file to ensure it looks correct.
```

### Step 2: Deploy Enhanced menu.py
```bash
# BACKUP FIRST (recommended)
copy "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py" "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py.backup"

# DEPLOY ENHANCED VERSION
copy "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke_DEV\\tractor\\enhanced_menu.py" "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py"
```

### Step 3: Test the Fix
```python
# In Nuke, run:
exec(open(r"\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke_DEV\\tractor\\test_connect_loading.py").read())
```

### Step 4: Test on Render Farm
Submit a simple job with Connect.gizmo nodes to verify it works on render blades.

### Step 5: Monitor Results
Check render logs for:
- "[CONNECT] Connect.gizmo successfully loaded!" messages
- Absence of "Connect.gizmo: unknown command" errors

## What This Fix Does

1. **Enhanced Loading**: Adds multiple fallback methods for loading Connect.gizmo
2. **Better Diagnostics**: Provides detailed logging of loading attempts  
3. **Render Farm Compatible**: Designed specifically for headless render environments
4. **Non-Breaking**: Preserves all existing functionality

## Rollback Plan

If any issues occur:
```bash
copy "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py.backup" "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\menu.py"
```

## Expected Results

After deployment:
- ✅ Connect.gizmo loads properly on all render farm nodes
- ✅ No more "unknown command" errors for Connect.gizmo  
- ✅ Existing scripts continue to work without modification
- ✅ Enhanced error reporting for troubleshooting

## Success Criteria

The fix is successful when:
1. test_connect_loading.py reports success in Nuke
2. Render farm jobs with Connect.gizmo complete without errors
3. Render logs show "[CONNECT] Connect.gizmo successfully loaded!"
'''
    
    guide_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\PERMANENT_FIX_DEPLOYMENT.md"
    
    try:
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)
        print(f"✅ Deployment guide created at: {guide_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create deployment guide: {e}")
        return False

def main():
    """Main function to implement the permanent solution"""
    
    print("=" * 80)
    print("PERMANENT CONNECT.GIZMO FIX - IMPLEMENTATION")
    print("=" * 80)
    
    print("\\nThis will create the permanent solution for Connect.gizmo loading issues.")
    print("The solution enhances the existing menu.py to ensure proper plugin loading.")
    
    # Step 1: Create backups
    if not backup_original_files():
        print("❌ Backup failed - aborting")
        return False
    
    # Step 2: Create enhanced menu.py
    if not create_enhanced_menu_py():
        print("❌ Enhanced menu.py creation failed")
        return False
    
    # Step 3: Create test script
    if not create_render_farm_test_script():
        print("❌ Test script creation failed")
        return False
    
    # Step 4: Create deployment guide
    if not create_deployment_guide():
        print("❌ Deployment guide creation failed")
        return False
    
    print("\\n" + "=" * 80)
    print("PERMANENT SOLUTION READY FOR DEPLOYMENT")
    print("=" * 80)
    
    print("\\n✅ Files created:")
    print("   - enhanced_menu.py (enhanced version with Connect.gizmo fix)")
    print("   - test_connect_loading.py (test script to verify fix works)")
    print("   - PERMANENT_FIX_DEPLOYMENT.md (deployment instructions)")
    
    print("\\n📋 Next Steps:")
    print("   1. Review enhanced_menu.py")
    print("   2. Deploy enhanced_menu.py to production")
    print("   3. Test with test_connect_loading.py")
    print("   4. Submit render job to verify fix works on farm")
    
    print("\\n🚀 Ready to deploy permanent Connect.gizmo fix!")
    
    return True

if __name__ == "__main__":
    main()
