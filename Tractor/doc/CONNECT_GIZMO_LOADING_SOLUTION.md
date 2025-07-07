# Connect.gizmo Plugin Loading Solution - June 26, 2025

## Issue Analysis
Based on the render logs, the problem is NOT that Connect.gizmo doesn't exist, but that it's not being loaded properly on the render farm despite NUKE_PATH being set correctly.

## Evidence from Logs
✅ **NUKE_PATH is working** - We see: `Loading \\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke/init.py`
❌ **Connect.gizmo not loading** - We see: `ERROR: Connect3: 'Connect.gizmo': unknown command`

## Root Cause
The Connect.gizmo file exists at `\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo` but it's not being registered/loaded by Nuke on the render blades.

## Analysis of Current Setup

### menu.py Analysis
The menu.py file contains:
```python
nuke.pluginAddPath('./nk_files')
```

This should make Connect.gizmo available, but it's failing on render blades.

## Potential Solutions

### Solution 1: Verify Gizmo File Accessibility (RECOMMENDED)
Test if the gizmo file is actually accessible on the render blades.

### Solution 2: Explicit Gizmo Loading
Add explicit gizmo loading in menu.py to force registration.

### Solution 3: Fix Plugin Loading Order
Ensure gizmos are loaded after all prerequisites.

### Solution 4: Alternative Plugin Path
Use absolute paths instead of relative paths for plugin loading.

## Immediate Action Plan

### Step 1: Create Gizmo Loading Test
Create a test script to verify if Connect.gizmo can be loaded on render blades.

### Step 2: Enhanced Menu.py (if needed)
Add explicit gizmo loading and error handling to menu.py.

### Step 3: Fallback Solution
Keep the emergency replacement scripts ready as backup.

## Diagnostic Commands
To test on a render blade:
```python
import nuke
print("Plugin paths:", nuke.pluginPath())
print("Available nodes:", sorted([n for n in dir(nuke.nodes) if 'Connect' in n]))
try:
    connect_node = nuke.nodes.Connect()
    print("Connect.gizmo loaded successfully")
except:
    print("Connect.gizmo failed to load")
```

## Next Steps
1. **Investigate menu.py execution** on render blades
2. **Test gizmo file accessibility** from render environment  
3. **Implement enhanced loading mechanism** if needed
4. **Maintain emergency replacement** as backup solution

This approach focuses on fixing the root cause rather than working around it, while keeping the emergency fixes available as backup.
