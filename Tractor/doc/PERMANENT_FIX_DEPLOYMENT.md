# PERMANENT CONNECT.GIZMO FIX - DEPLOYMENT GUIDE

## Quick Deployment Steps

### Step 1: Review Enhanced menu.py
```
enhanced_menu.py has been created with the permanent fix.
Review this file to ensure it looks correct.
```

### Step 2: Deploy Enhanced menu.py
```bash
# BACKUP FIRST (recommended)
copy "\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\menu.py" "\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\menu.py.backup"

# DEPLOY ENHANCED VERSION
copy "\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\enhanced_menu.py" "\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\menu.py"
```

### Step 3: Test the Fix
```python
# In Nuke, run:
exec(open(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\test_connect_loading.py").read())
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
copy "\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\menu.py.backup" "\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\menu.py"
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
