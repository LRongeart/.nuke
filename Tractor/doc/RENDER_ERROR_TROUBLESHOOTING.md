# Render Error Troubleshooting Guide

## Common RenderiThe render command now includes these improvements:
```bash
"C:\Program Files\Nuke15.1v2\Nuke15.1.exe" -V 2 -x script.nk -F 1-1 -X Write1
```

**Environment Variables Set:**
- `NUKE_PATH=\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke`
- `PYTHONPATH=\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke`

**Important Changes:**
- **Removed `--nukex`** to avoid licensing issues on render farm
- **Single frame per task** (`-F 1-1`) for better compatibility
- **Enhanced format detection** to warn about video formats

**Command Breakdown:**ues and Solutions

### Issue 1: "Connect.gizmo: unknown command" Error - UPDATED ANALYSIS

**Problem:** 
```
ERROR: Connect3: 'Connect.gizmo': unknown command. This is most likely from a corrupt .nk file, or from a missing or unlicensed plug-in.
```

**UPDATED Root Cause Analysis (June 26, 2025):**
- Connect.gizmo EXISTS at `\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo`  
- menu.py includes `nuke.pluginAddPath('./nk_files')` 
- NUKE_PATH environment variable is set correctly
- Custom init.py IS loading (confirmed in logs)
- **ISSUE**: Gizmo loading timing or registration problem on render farm

**Evidence from Logs:**
✅ NUKE_PATH working: `Loading \\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke/init.py`
❌ Connect.gizmo failing: `Connect.gizmo: unknown command`

**Solutions Implemented:**
1. **Added plugin path to render command** - The render command now includes:
   ```
   --plugin-path \\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke
   ```
2. **NUKE_PATH environment variable** - Set for each render task
3. **Verbose output enabled** - Added `-V 2` flag for better debugging

**Additional Solutions to Consider:**
- Ensure gizmos are available on network storage accessible by all blades
- Consider "baking" gizmos into the script before rendering
- Use Nuke's built-in nodes instead of custom gizmos when possible

### Issue 2: "You must specify a file name to write to" Error

**Problem:** 
```
You must specify a file name to write to.
```

**Root Cause:** The Write node doesn't have a proper output file path specified.

**Solutions Implemented:**
1. **Enhanced Write node validation** - Added checks for:
   - Both 'file' knob and evaluated paths using `write_node.filename()`
   - Relative vs absolute path detection
   - Proper path resolution for render farm compatibility

2. **Relative path handling** - Uses Nuke's `filename()` method to resolve paths

3. **Network path validation** - Added warnings if script is not on a network location

**User Actions Required:**
1. **Set Output Path in Write Node:**
   - Open the Write node properties
   - Set the "file" field to a valid output path
   - Use network paths like `\\tls-storage02\RENDER\project_name\shot_name\v001\frame.####.exr`

2. **Save Script to Network Location:**
   - Save your .nk file to a network location accessible by render blades
   - Recommended: `\\tls-storage02\...` paths

## Updated Command Structure

The render command now includes these improvements:
```bash
"C:\Program Files\Nuke15.1v2\Nuke15.1.exe" --nukex -V 2 --plugin-path \\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke -x script.nk -F 1001-1001 -X Write1
```

**Command Breakdown:**
- `--nukex` - ~~Removed due to licensing issues on render farm~~
- `-V 2` - Verbose output for debugging
- `-x` - Execute script
- `-F` - Frame range (single frame per task)
- `-X` - Write node name

**Environment Variables:**
- `NUKE_PATH` - Provides access to custom plugins and gizmos
- `PYTHONPATH` - Provides access to custom Python modules

### Issue 3: "Write2 cannot be executed for multiple frames"

**Problem:**
```
Write2 cannot be executed for multiple frames.
```

**Root Cause:** Write node is configured for video output (MOV, MP4, AVI) which doesn't support frame-by-frame rendering.

**Solutions Implemented:**
1. **Format detection** - System now detects and warns about video formats
2. **User guidance** - Suggests using image sequence formats instead
3. **Single frame tasks** - Each task renders one frame instead of ranges

**User Actions Required:**
- Change Write node format from MOV to EXR, TIFF, or PNG
- Use frame padding in filename: `output.####.exr`

## Debugging Steps

1. **Check Write Node Setup:**
   ```python
   # In Nuke script console:
   write_node = nuke.toNode('Write1')
   print("File path (knob):", write_node['file'].value())
   print("File path (evaluated):", write_node.filename())
   ```

2. **Handle Relative Paths:**
   - The system now automatically resolves relative paths using `write_node.filename()`
   - Relative paths are detected and warnings are shown
   - Consider using absolute network paths for better compatibility

2. **Verify Plugin Availability:**
   - Check if gizmos exist in: `\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke`
   - Test script locally with same plugin paths

3. **Test Minimal Render:**
   - Create a simple script with basic nodes only
   - Test if render works without custom gizmos

## Best Practices

1. **File Paths:**
   - Always use network paths for scripts and output
   - Use forward slashes or double backslashes in paths
   - Include frame padding: `####` or `%04d`

2. **Plugin Management:**
   - Keep custom gizmos in shared network locations
   - Document plugin dependencies
   - Consider "baking" complex node trees

3. **Testing:**
   - Test render locally before submitting to farm
   - Use single frame tests first
   - Check all Write nodes have valid paths

## Next Steps

If issues persist:
1. Check Tractor job logs for detailed error messages
2. Test script manually on a render blade
3. Verify network access to all required files
4. Consider simplifying the node graph to isolate issues
