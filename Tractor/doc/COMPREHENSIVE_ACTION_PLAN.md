# COMPREHENSIVE RENDER FIX ACTION PLAN - June 26, 2025

## Current Status Understanding ✅

**CONFIRMED FACTS:**
- ✅ Connect.gizmo file EXISTS at `\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo`
- ✅ menu.py includes `nuke.pluginAddPath('./nk_files')`  
- ✅ NUKE_PATH environment variable is set correctly
- ✅ Custom init.py IS loading on render farm (confirmed in logs)
- ❌ Connect.gizmo still fails with "unknown command" (plugin loading issue)
- ❌ Write2 node missing file path

## 🎯 SOLUTION APPROACH

Instead of just replacing the Connect.gizmo nodes, we have TWO parallel approaches:

### Approach A: Fix Plugin Loading (PREFERRED)
Fix the root cause so Connect.gizmo works properly on render farm

### Approach B: Emergency Workaround (BACKUP)  
Replace Connect.gizmo nodes if plugin loading cannot be fixed quickly

## 📋 IMMEDIATE ACTION PLAN

### STEP 1: Diagnose Plugin Loading (5 minutes)
```bash
# Run diagnostic on render farm
python plugin_loading_diagnostic.py
```
**Purpose:** Determine exactly why Connect.gizmo isn't loading despite proper paths

### STEP 2A: Enhanced Plugin Loading (10 minutes) 
If diagnostic shows loading issues:
```python
# Run in Nuke Script Editor
exec(open(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\enhanced_plugin_loading.py").read())
```
**Purpose:** Force proper Connect.gizmo loading

### STEP 2B: Emergency Replacement (5 minutes)
If plugin loading cannot be fixed immediately:
```python
# Run in Nuke Script Editor  
exec(open(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\EMERGENCY_CONNECT_FIX.py").read())
```
**Purpose:** Replace all 16 Connect.gizmo nodes with Dot nodes

### STEP 3: Fix Write Node Paths (5 minutes)
```python
# Run in Nuke Script Editor
exec(open(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\EMERGENCY_WRITE_FIX.py").read())
```
**Purpose:** Ensure Write2 node has proper output file path

### STEP 4: Test & Re-submit
1. Save Nuke script
2. Re-submit to Tractor  
3. Monitor logs for success

## 📊 DECISION MATRIX

| Issue | Preferred Solution | Emergency Solution | Time to Fix |
|-------|-------------------|-------------------|-------------|
| Connect.gizmo | Enhanced plugin loading | Replace with Dot nodes | 10 min vs 5 min |
| Write paths | Auto-path resolution | Manual path setting | 5 min |
| **TOTAL** | **15 minutes** | **10 minutes** | |

## 🔍 DIAGNOSTIC CHECKLIST

**Before choosing approach, verify:**
- [ ] Connect.gizmo file exists and is readable
- [ ] menu.py is executing on render blades  
- [ ] Plugin paths are correctly resolved
- [ ] Gizmo registration is working

**Quick test command:**
```python
import nuke, os
print("Gizmo exists:", os.path.exists(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo"))
print("Can create Connect:", hasattr(nuke.nodes, 'Connect'))
```

## ⚡ FASTEST SOLUTION PATH

**If you need immediate results (10 minutes):**
1. Run `EMERGENCY_CONNECT_FIX.py` (replace all Connect.gizmo → Dot)
2. Run `EMERGENCY_WRITE_FIX.py` (fix Write node paths)  
3. Save & re-submit to Tractor
4. Renders should work immediately

**If you want proper fix (15 minutes):**
1. Run `plugin_loading_diagnostic.py` (understand the issue)
2. Run `enhanced_plugin_loading.py` (fix plugin loading)
3. Run `EMERGENCY_WRITE_FIX.py` (fix Write node paths)
4. Save & re-submit to Tractor  
5. Connect.gizmo will work properly for future renders

## 📁 SCRIPT LOCATIONS

```
\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\
├── plugin_loading_diagnostic.py     ← Diagnose plugin issues
├── enhanced_plugin_loading.py       ← Fix plugin loading  
├── EMERGENCY_CONNECT_FIX.py         ← Replace Connect.gizmo
├── EMERGENCY_WRITE_FIX.py           ← Fix Write paths
└── EMERGENCY_FIX_GUIDE.md           ← Step-by-step guide
```

## 🎯 RECOMMENDATION

**For immediate render success:** Use Emergency Solutions (10 min)
**For long-term stability:** Use Enhanced Plugin Loading (15 min)

Both approaches will get your renders working today!
