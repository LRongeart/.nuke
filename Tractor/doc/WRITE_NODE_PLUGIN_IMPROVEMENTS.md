# Write Node & Plugin Path Improvements - COMPLETED

## Issues Addressed

### 1. Write Node Path Resolution
**Problem**: Write nodes sometimes have paths in relative format rather than absolute paths, causing "You must specify a file name to write to" errors.

**Solution Implemented**:
- Enhanced write node validation to check both `file` knob and evaluated paths
- Added `write_node.filename()` method to resolve relative paths to absolute paths
- Added warnings for relative paths while still allowing them to proceed
- Improved error messages for missing or invalid output paths

### 2. Custom Tools/Gizmos Plugin Path
**Problem**: Custom gizmos like "Connect.gizmo" not found on render blades, causing "unknown command" errors.

**Solution Implemented**:
- Added `--plugin-path` argument pointing to the correct custom tools folder
- Set `NUKE_PATH` environment variable for each render task
- Updated plugin path to use the correct location: `\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke`

## Code Changes

### File: `submit_to_tractor_ui.py`

**Enhanced Write Node Validation** (lines 493-520):
```python
# Check both 'file' knob and potential relative path knobs
file_path = ""
if 'file' in write_node.knobs():
    file_path = write_node['file'].value()

# If file path is empty or relative, try to get the full path
if not file_path or not os.path.isabs(file_path):
    try:
        # Use Nuke's filename() method to get the evaluated path
        file_path = write_node.filename()
    except:
        pass
```

**Updated Command Structure** (lines 594-614):
```python
# Build command with proper environment and plugin paths
nuke_plugin_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke"

cmd = [
    nuke_exe, "--nukex", 
    "-V", "2",  # Enable verbose output for debugging
    "--plugin-path", nuke_plugin_path,
    "-x", script_path,
    "-F", f"{frame}-{frame}",
    "-X", write_name
]
```

**Environment Variable Setup** (lines 615-628):
```python
# Set NUKE_PATH environment variable
env_vars = {
    'NUKE_PATH': nuke_plugin_path
}
```

## Updated Render Command

The complete render command now includes:
```bash
"C:\Program Files\Nuke15.1v2\Nuke15.1.exe" --nukex -V 2 --plugin-path \\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke -x script.nk -F 1001-1001 -X Write1
```

**Environment Variables**:
- `NUKE_PATH=\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke`

## Expected Results

### For Write Node Issues:
- ✅ Automatic resolution of relative paths to absolute paths
- ✅ Better validation and error messages for missing paths
- ✅ Support for both direct file knob values and evaluated paths
- ✅ Warnings for relative paths while still allowing submission

### For Plugin/Gizmo Issues:
- ✅ Custom gizmos and tools should be available to render blades
- ✅ Connect.gizmo and other custom tools should load properly
- ✅ NUKE_PATH environment variable set for each render task
- ✅ Verbose output for better debugging of plugin loading

## Testing Steps

1. **Test Write Node Path Resolution**:
   ```python
   # In Nuke console:
   write_node = nuke.toNode('Write1')
   print("Direct file value:", write_node['file'].value())
   print("Resolved filename:", write_node.filename())
   ```

2. **Test Custom Gizmo Loading**:
   - Submit a job with a script using Connect.gizmo
   - Check render logs for plugin loading messages
   - Verify no "unknown command" errors

3. **Monitor Environment Variables**:
   - Check Tractor job logs for NUKE_PATH setting
   - Verify plugin path is included in command line

## File Status
- ✅ `submit_to_tractor_ui.py` - Updated with enhanced write node validation and plugin paths
- ✅ `RENDER_ERROR_TROUBLESHOOTING.md` - Updated with new solutions
- ✅ Syntax validation passed
- 🔄 Ready for testing with problematic scripts

This should resolve both the relative path issues and the custom gizmo loading problems.
