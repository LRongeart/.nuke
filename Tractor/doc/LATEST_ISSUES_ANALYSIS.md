# Latest Render Issues - Analysis & Solutions

## Issues Identified from Latest Log

### 1. Connect.gizmo Still Not Loading
```
ERROR: Connect15: 'Connect.gizmo': unknown command.
```

**Analysis:** Even though plugins are loading, the specific Connect.gizmo is not being found.

**Solutions:**
1. **Check gizmo location**: Verify Connect.gizmo exists in `\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke`
2. **Alternative approach**: Replace Connect nodes with standard Nuke nodes before rendering
3. **Pre-render script**: Add a script to "bake" gizmos into standard nodes

### 2. Write Node Multi-Frame Issue
```
Write2 cannot be executed for multiple frames.
```

**Root Cause:** The Write node is configured for single-frame output (likely MOV format) but being asked to render frame ranges.

**Solutions Implemented:**
- Enhanced Write node validation to detect video formats
- Warning dialog for problematic formats (MOV, MP4, AVI)
- Suggestion to use image sequence formats (EXR, TIFF, PNG)

### 3. NukeX Licensing Issue
```
NOTE : NukeX functionality is only available with an interactive license.
```

**Solution Applied:** Removed `--nukex` flag to use regular Nuke license for render farm.

## Updated Solutions

### ✅ **Command Structure Fixed:**
```bash
"C:\Program Files\Nuke15.1v2\Nuke15.1.exe" -V 2 -x script.nk -F 1-1 -X Write2
```
**Changes:**
- Removed `--nukex` (licensing issue)
- Kept `-V 2` for debugging
- Single frame per task: `-F 1-1` instead of ranges

### ✅ **Write Node Format Detection:**
- Automatically detects video formats (MOV, MP4, AVI)
- Warns user about frame-by-frame rendering incompatibility
- Suggests image sequence formats

### ✅ **Enhanced Environment Variables:**
```
NUKE_PATH=\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke
PYTHONPATH=\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke
```

## Immediate Actions Required

### 1. **Fix Write Node Format**
**Current Issue:** Write2 is likely set to MOV format
**Solution:** Change Write2 to:
- **Format**: EXR, TIFF, or PNG
- **File path**: Use image sequence with frame padding
- **Example**: `output.####.exr` instead of `output.mov`

### 2. **Handle Connect.gizmo**
**Option A - Replace manually:**
```python
# In Nuke script console:
for node in nuke.allNodes():
    if node.Class() == 'Group' and 'Connect' in node.name():
        print(f"Found Connect node: {node.name()}")
        # Replace with standard nodes
```

**Option B - Ensure gizmo is available:**
- Check if `Connect.gizmo` exists in the plugin directory
- Verify it's properly loaded during initialization

### 3. **Test Command**
Try manually on a blade:
```bash
"C:\Program Files\Nuke15.1v2\Nuke15.1.exe" -V 2 -x "script.nk" -F 1-1 -X Write2
```

## Expected Results After Fixes

1. **No more licensing errors** (removed --nukex)
2. **Proper frame-by-frame rendering** (if Write node format is fixed)
3. **Better plugin loading** (with enhanced environment variables)

## Next Steps

1. **Update Write2 node** to use EXR format with frame padding
2. **Test single frame render** before submitting full job
3. **Check Connect.gizmo availability** in plugin directory
4. **Consider replacing Connect nodes** with standard Nuke nodes

The main blocker now is likely the Write node format issue. Once that's resolved to use an image sequence format, the renders should work properly.
