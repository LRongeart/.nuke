# EMERGENCY RENDER FIX GUIDE - June 26, 2025

## CRITICAL ISSUES IDENTIFIED

Your Tractor renders are failing due to two critical issues that need immediate attention:

### 🔴 ISSUE 1: Connect.gizmo Errors (16 nodes affected)
**Error:** `Connect.gizmo: unknown command`
**Impact:** Prevents any rendering from starting

### 🔴 ISSUE 2: Write Node Missing File Path  
**Error:** `You must specify a file name to write to`
**Impact:** Even if Connect.gizmo is fixed, renders will fail

## 🚀 IMMEDIATE SOLUTION STEPS

### Step 1: Fix Connect.gizmo Nodes (5 minutes)

1. **Open your failing Nuke script**
2. **Open Script Editor:** Window → Python Editor
3. **Copy and paste this entire file:** `EMERGENCY_CONNECT_FIX.py`
4. **Click Run** - This will replace all 16 Connect.gizmo nodes with Dot nodes
5. **Verify:** Check that no Connect.gizmo nodes remain in your node graph

### Step 2: Fix Write Node Paths (5 minutes)

1. **In the same Nuke script**
2. **In Script Editor, copy and paste:** `EMERGENCY_WRITE_FIX.py`  
3. **Click Run** - This will find and help fix Write node file paths
4. **Follow prompts** to set proper output paths for Write nodes
5. **Verify:** Ensure all Write nodes have valid file paths

### Step 3: Re-submit to Tractor

1. **Save your script** (Ctrl+S)
2. **Use the Tractor submission UI** 
3. **Submit job** - Should now render successfully
4. **Monitor logs** for success confirmation

## 📁 EMERGENCY SCRIPTS LOCATION

```
\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\
├── EMERGENCY_CONNECT_FIX.py    ← Fix Connect.gizmo errors
├── EMERGENCY_WRITE_FIX.py      ← Fix Write node paths  
└── THIS_FILE.md                ← This guide
```

## ⚡ QUICK COPY-PASTE SOLUTIONS

### Connect.gizmo Quick Fix (Paste in Nuke Script Editor):
```python
import nuke
for node in nuke.allNodes():
    if 'Connect' in node.Class() and 'gizmo' in node.Class().lower():
        dot = nuke.nodes.Dot()
        dot.setXpos(node.xpos())
        dot.setYpos(node.ypos()) 
        if node.inputs() > 0:
            dot.setInput(0, node.input(0))
        for dep in nuke.allNodes():
            for i in range(dep.inputs()):
                if dep.input(i) == node:
                    dep.setInput(i, dot)
        nuke.delete(node)
print("Connect.gizmo nodes replaced!")
```

### Write Node Quick Check (Paste in Nuke Script Editor):
```python
import nuke
for node in nuke.allNodes():
    if node.Class() == 'Write':
        path = node['file'].value()
        if not path:
            print(f"ERROR: {node.name()} has no file path!")
        else:
            print(f"OK: {node.name()} → {path}")
```

## 🔍 VERIFICATION CHECKLIST

Before re-submitting:
- [ ] No Connect.gizmo nodes in script (check Node Graph)
- [ ] All Write nodes have file paths set
- [ ] File paths are absolute (not relative)
- [ ] Output directories exist and are accessible
- [ ] Script saved after fixes

## 📊 SUCCESS INDICATORS

After re-submission, look for:
- ✅ Job picked up by blade
- ✅ Nuke starts without "unknown command" errors  
- ✅ Write nodes begin output without "file name" errors
- ✅ Frames render successfully
- ✅ Output files appear in specified directories

## 🆘 IF STILL FAILING

1. **Check logs** in Tractor web interface
2. **Run diagnostics:** `TRACTOR_DIAGNOSTICS.py`
3. **Contact pipeline support** with:
   - Tractor job ID
   - Render log excerpts
   - Nuke script path

## 📞 SUPPORT CONTACT

Pipeline Team: [Insert contact info]
Tractor Web Interface: [Insert URL]

---
**This guide resolves the immediate render failures. Both fixes are safe and preserve your node graph functionality while eliminating render farm compatibility issues.**
