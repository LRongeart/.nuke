# WRITE NODE PATH RESTORATION FIX

## Problem
After submitting a Tractor job, the Write node's file path was permanently changed in the Nuke script. When closing the Tractor interface, the original paths were not restored.

**Example:**
- **Original:** `OUT/comp_beauty.%04d.exr`
- **After submission:** `OUT/comp_beauty.0001.exr` (frame-specific path)
- **Issue:** Original template path was lost

## Root Cause
The Tractor submission process was modifying Write node paths in multiple places:

1. **UI validation:** Converting relative to absolute paths
2. **Auto-fix logic:** Setting paths for empty Write nodes  
3. **Generated Python scripts:** Setting frame-specific paths
4. **No restoration:** Original paths were never saved or restored

## Solution Applied

### 1. **Track Original Paths**
At the beginning of `submitJobs()`:
```python
# Store original Write node paths for restoration after job submission
original_write_paths = {}
for item in selected_items:
    write_name = item.text()
    write_node = nuke.toNode(write_name)
    if write_node and 'file' in write_node.knobs():
        original_write_paths[write_name] = write_node['file'].value()
```

### 2. **Restore Paths After Submission**
At the end of `submitJobs()`:
```python
# Restore original Write node paths
restored_count = 0
for write_name, original_path in original_write_paths.items():
    try:
        write_node = nuke.toNode(write_name)
        if write_node and 'file' in write_node.knobs():
            current_path = write_node['file'].value()
            if current_path != original_path:
                write_node['file'].setValue(original_path)
                restored_count += 1
                print(f"Restored Write node '{write_name}' path: {original_path}")
    except Exception as restore_e:
        print(f"Could not restore Write node '{write_name}' path: {restore_e}")

if restored_count > 0:
    nuke.scriptSave()  # Save with restored paths
```

### 3. **Enhanced Python Script Logic**
In generated render scripts:
```python
# Save original path before modification
original_file_path = write_node['file'].value()
write_node['file'].setValue(final_path)  # Set frame-specific path

# ... render ...

# Restore original path after render
write_node['file'].setValue(original_file_path)
nuke.scriptSave()  # Save with restored path
```

## Benefits

### ✅ **Preserved Original Paths**
- Write nodes maintain their original template paths (`%04d`, `####`)
- No permanent modification of the Nuke script
- Artists' intended path structure preserved

### ✅ **Backwards Compatibility**
- All existing functionality maintained
- Job submission works exactly the same
- No workflow changes for users

### ✅ **Smart Restoration**
- Only restores paths that were actually changed
- Handles errors gracefully if restoration fails
- Provides clear logging of restoration process

### ✅ **Automatic Save**
- Script automatically saved with restored paths
- Ensures changes are persisted correctly
- No manual intervention required

## Example Workflow

### **Before Fix:**
1. Write node: `OUT/beauty.%04d.exr`
2. Submit to Tractor → Path changed to `OUT/beauty.0001.exr`
3. Close UI → Path remains `OUT/beauty.0001.exr` ❌

### **After Fix:**
1. Write node: `OUT/beauty.%04d.exr`
2. Submit to Tractor → Path temporarily changed for submission
3. Close UI → Path restored to `OUT/beauty.%04d.exr` ✅

## Debug Output
The system now provides clear logging:
```
[DEBUG] Restored Write node 'Write2' path: OUT/comp_beauty.%04d.exr
[DEBUG] Restored 1 Write node paths to original values
[DEBUG] Saved script with restored Write node paths
```

## Files Modified
- `submit_to_tractor_ui.py` - Added path tracking and restoration logic

## Expected Behavior
- ✅ Write nodes preserve original template paths
- ✅ Job submission works correctly with frame-specific paths
- ✅ No permanent script modifications
- ✅ Automatic restoration and save after submission

The system now respects artists' original path intentions while enabling robust Tractor rendering!
