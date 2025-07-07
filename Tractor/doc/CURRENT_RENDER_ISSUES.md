# Current Render Issues Analysis - June 26, 2025 17:00

## Summary
Jobs are successfully submitting to Tractor and being picked up by blades, but failing during render due to two critical issues:

## Issue 1: Connect.gizmo Errors (CRITICAL)
**Error Message:**
```
ERROR: Connect3: 'Connect.gizmo': unknown command. This is most likely from a corrupt .nk file, or from a missing or unlicensed plug-in.
```

**Analysis:**
- 16 Connect.gizmo nodes found in the script
- These gizmos are not available on the render farm
- Causing immediate render failure

**Impact:** High - Prevents any rendering from completing

## Issue 2: Write Node Missing File Path (CRITICAL)
**Error Message:**
```
You must specify a file name to write to.
```

**Analysis:**
- Write2 node lacks a proper output file path
- This is a configuration issue in the Nuke script

**Impact:** High - Even if Connect.gizmo issue is fixed, renders will fail

## Immediate Action Items

### 1. Fix Connect.gizmo Issues
**Option A: Auto-replace with Dot nodes (RECOMMENDED)**
- Use the fix_connect_gizmo.py script
- Automatically replace Connect.gizmo nodes with Dot nodes
- Preserve connections while removing problematic gizmos

**Option B: Manual replacement**
- Open script in Nuke
- Find all Connect.gizmo nodes
- Replace with standard Nuke nodes (Dot, Merge, etc.)

### 2. Fix Write Node Paths
**Required Actions:**
- Ensure all Write nodes have valid output file paths
- Convert relative paths to absolute paths
- Verify paths are accessible on render farm

## Recovery Scripts Available

1. **fix_connect_gizmo.py** - Auto-replaces Connect.gizmo nodes
2. **CONNECT_GIZMO_SOLUTION.py** - Troubleshooting and manual fix guide
3. **submit_to_tractor_ui.py** - Enhanced validation for Write nodes

## Next Steps
1. Run fix_connect_gizmo.py on the Nuke script
2. Verify Write node output paths are properly configured
3. Re-submit job to Tractor
4. Monitor render logs for success

## Log Locations
- Tractor logs: Available through Tractor web interface
- Blade logs: Check render farm blade log directories
- Debug output: Enabled in submit_to_tractor_ui.py
