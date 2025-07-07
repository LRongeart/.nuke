# Show List Empty - Troubleshooting Guide

## Issue
The project/show dropdown list appears empty in the Tractor submission UI.

## Root Cause Analysis
The UI looks for project lists in this order:
1. `~/.nuke/tractor/live_projects.json` (user-specific)
2. `\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\live_projects.json` (shared)
3. Auto-detection from current script path
4. Default project list fallback

## Solutions Implemented

### ✅ **Enhanced Project Loading**
```python
def populateProjects(self):
    # Try multiple sources in order of preference
    # 1. User-specific project file
    # 2. Shared project file 
    # 3. Auto-detection from script path
    # 4. Default fallback list
```

### ✅ **Auto-Detection from Script Path**
For your current script: `//tls-storage02/3D2/_NUKE/3D2_NUKE_010_CG/ESMA_10_3D3_RebuildEnvironment/RebuildEnvironment_COMP_v001.nk`

The system will automatically detect: **"3D2"** or **"3D3"** as the project name.

### ✅ **Fallback Project List**
If all else fails, the system will show:
- EXIT
- 3D2  
- 3D3
- COMP
- RENDER

## Available Projects
The shared `live_projects.json` contains:
```json
[
    "SHOW_TEST",
    "EXIT", 
    "TUMACO",
    "FLOWER",
    "PUMPKIN",
    "MIXUP",
    "3D3",
    "3D4"
]
```

## Debug Information
The UI will now show debug messages in the console:
```
[Tractor UI] -Opt1- Looking for project file at: ~/.nuke/tractor/live_projects.json
[Tractor UI] -Opt2- Looking for project file at: \\tls-storage02\...\live_projects.json
[Tractor UI] Loaded 8 projects from live_projects.json
```

Or if auto-detecting:
```
[Tractor UI] No project file found, attempting auto-detection...
[Tractor UI] Auto-detected project: 3D2
```

## Manual Solutions

### **Option 1: Create User-Specific Project File**
Create: `~/.nuke/tractor/live_projects.json`
```json
["YOUR_PROJECT", "3D2", "3D3", "EXIT"]
```

### **Option 2: Edit Shared Project File**
Update: `\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\live_projects.json`
Add your project names to the existing list.

### **Option 3: Manual Entry**
The project field is editable - you can type your project name directly.

## Testing

### **Restart the UI and check for:**
1. **Debug messages** in the Nuke console showing project loading
2. **Populated dropdown** with available projects
3. **Auto-detected project** based on your current script path

### **If still empty:**
1. Check console for error messages
2. Verify file permissions on the live_projects.json
3. Try typing the project name manually (the field is editable)

## Expected Result
After the fix, your project dropdown should show the available projects, and for your current script, it should auto-detect "3D2" or "3D3" as the appropriate project.

The project field is also editable, so you can always type in a custom project name if needed.
