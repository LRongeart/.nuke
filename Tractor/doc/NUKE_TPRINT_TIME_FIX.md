# NUKE.TPRINT_TIME ERROR FIX

## Problem
Render script failed with:
```
AttributeError: module 'nuke' has no attribute 'tprint_time'
```

## Root Cause
The generated Python script was trying to use `nuke.tprint_time()` which doesn't exist in Nuke's Python API.

**Incorrect code:**
```python
start_time = nuke.tprint_time()
# ... render ...
end_time = nuke.tprint_time()
```

## Solution Applied

### Fixed Timing Logic
**OLD (Broken):**
```python
start_time = nuke.tprint_time()  # ❌ Function doesn't exist
nuke.execute(write_node, frame, frame)
end_time = nuke.tprint_time()    # ❌ Function doesn't exist
```

**NEW (Working):**
```python
import time
start_time = time.time()         # ✅ Standard Python function
nuke.execute(write_node, frame, frame)
end_time = time.time()           # ✅ Standard Python function
render_duration = end_time - start_time
print("Render time: %.2f seconds" % render_duration)
```

## Analysis of Log

Looking at the error log, the render was actually proceeding correctly:

### ✅ **What Worked:**
- Script opened successfully
- Write node found correctly
- Path evaluation worked: `OUT/RebuildEnvironment_COMP_v001_Write2.%04d.exr` → `OUT/RebuildEnvironment_COMP_v001_Write2.0001.exr`
- Output directory exists
- File path set correctly

### ❌ **What Failed:**
- Only the timing measurement with non-existent `nuke.tprint_time()`

## Important Observations

### **Write Node Path Handling Working:**
The log shows our path handling is working correctly:
```
Original file path: OUT/RebuildEnvironment_COMP_v001_Write2.%04d.exr
Final output path: OUT/RebuildEnvironment_COMP_v001_Write2.0001.exr
Output directory exists: OUT
```

This confirms:
- ✅ Relative path `OUT/` is being handled properly
- ✅ Frame number substitution working (`%04d` → `0001`)
- ✅ Directory detection working
- ✅ Our path handling respects existing Write node paths

### **Connected.gizmo Loading Working:**
No plugin errors in the log, confirming our Connect.gizmo fixes are working.

## Files Modified
- `submit_to_tractor_ui.py` - Fixed timing logic in generated Python scripts
- `test/test_timing_fix.py` - NEW test to verify timing functionality

## Testing Results
- ✅ Test script confirms timing fix works correctly
- ✅ Syntax check passes
- ✅ Duration measurement accurate (1.00 seconds for 1-second test)

## Expected Result
Now when you submit a job:
1. ✅ Python scripts generated correctly
2. ✅ No `nuke.tprint_time()` errors
3. ✅ Render timing measured accurately
4. ✅ All existing functionality preserved

The render should now complete successfully without the AttributeError!
