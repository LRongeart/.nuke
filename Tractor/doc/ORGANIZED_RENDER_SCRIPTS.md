# ORGANIZED PYTHON RENDER SCRIPTS

## Overview

The Tractor submission system now creates organized Python render scripts in a structured folder hierarchy instead of cluttering the script directory with temporary files.

## Folder Structure

When you submit a Tractor job, Python render scripts are now stored in:

```
/path/to/your/nuke/script/
├── YourScript.nk
├── py/
│   └── YourScript/                    # Folder named after your .nk script
│       ├── render_Write1_f001_1234567890.py
│       ├── render_Write1_f002_1234567890.py
│       ├── render_Write2_f001_1234567890.py
│       └── render_Write2_f002_1234567890.py
└── renders/                           # Output folder for rendered frames
    ├── YourScript_Write1.0001.exr
    ├── YourScript_Write1.0002.exr
    ├── YourScript_Write2.0001.exr
    └── YourScript_Write2.0002.exr
```

## File Naming Convention

Each Python render script follows this naming pattern:
```
render_{WriteNodeName}_f{FrameNumber}_{Timestamp}.py
```

Examples:
- `render_Write2_f001_1719428123.py` - Renders frame 1 of Write2 node
- `render_BeautyPass_f024_1719428124.py` - Renders frame 24 of BeautyPass node

## Benefits

### 1. **Organization**
- All render scripts are grouped by the originating Nuke script
- Easy to find and debug specific render issues
- No more cluttered script directories

### 2. **Debugging**
- Each script contains detailed metadata about the render job
- Clear logging with timestamps and progress information
- Scripts remain after render for debugging (auto-cleanup on success)

### 3. **Maintenance**
- Automated cleanup utility removes old scripts
- Easy to see render history for each script
- Timestamp prevents filename conflicts

## Render Script Features

Each generated Python script includes:

### **Metadata Header**
```python
"""
Tractor Nuke Render Script
Generated: 2025-06-26 18:15:23
Script: RebuildEnvironment_COMP_v001.nk
Write Node: Write2
Frame: 1
"""
```

### **Detailed Logging**
- Script opening status
- Write node validation
- Path evaluation and correction
- Directory creation if needed
- Render progress and timing
- Output file verification

### **Robust Error Handling**
- Clear error messages for troubleshooting
- Automatic directory creation
- Path format detection and correction
- File existence verification

### **Self-Cleanup**
- Successful renders automatically delete their script files
- Failed renders leave scripts for debugging
- Manual cleanup utility available

## Cleanup Utility

Use `cleanup_render_scripts.py` to manage old render scripts:

### **In Nuke Script Editor:**
```python
# Load and run cleanup utility
exec(open(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\cleanup_render_scripts.py").read())

# Cleanup current project (dry run first)
cleanup_current_project(days_old=7, dry_run=True)

# Actually delete old files
cleanup_current_project(days_old=7, dry_run=False)
```

### **From Command Line:**
```bash
cd "path/to/tractor/scripts"
nuke.exe -t cleanup_render_scripts.py
```

### **Batch Cleanup All Projects:**
```python
# Cleanup all projects under a root directory
cleanup_all_projects(r"\\tls-storage02\3D2\_NUKE", days_old=7, dry_run=False)
```

## Tractor Integration

The organized structure works seamlessly with Tractor:

1. **Job Submission**: Creates `py/<script_name>/` directory automatically
2. **Render Execution**: Tractor runs the specific Python script for each frame
3. **Success Cleanup**: Scripts self-delete after successful renders
4. **Failure Debugging**: Failed scripts remain for analysis

## Example Tractor Command

**OLD COMMAND:**
```
nuke.exe -x script.nk -F 1-1 -X Write2
```

**NEW COMMAND:**
```
nuke.exe -t py/RebuildEnvironment_COMP_v001/render_Write2_f001_1719428123.py
```

## Troubleshooting

### **Script Not Found**
- Check if the `py/<script_name>/` directory exists
- Verify write permissions on the script directory
- Look for error messages in Tractor job logs

### **Old Scripts Accumulating**
- Run the cleanup utility regularly
- Check if auto-cleanup is working (scripts should self-delete on success)
- Consider setting up a scheduled cleanup task

### **Permission Issues**
- Ensure render blades have write access to the script directory
- Check network path accessibility from render farm
- Verify folder creation permissions

## Best Practices

1. **Regular Cleanup**: Run cleanup utility weekly or monthly
2. **Monitor Disk Usage**: Python scripts are small but can accumulate
3. **Debug Failed Renders**: Check remaining script files for error clues
4. **Backup Important Scripts**: Save useful debugging scripts before cleanup
5. **Network Paths**: Always use absolute network paths for farm compatibility

This organized approach makes Tractor rendering more reliable, debuggable, and maintainable!
