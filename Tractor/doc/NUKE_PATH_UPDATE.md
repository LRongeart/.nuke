# Nuke Executable Path Update - COMPLETED

## Issue
Blades were unable to find `nuke.exe`, resulting in "exec failed - program executable not found: nuke.exe" errors when trying to execute Tractor jobs.

## Root Cause
The job submission code was using an incorrect path to the Nuke executable:
- **Old path**: `C:\Program Files\Nuke15.1v1\nuke.exe`
- **Correct path**: `C:\Program Files\Nuke15.1v2\Nuke15.1.exe`

Additionally, the user specified that the `--nukex` argument should be used.

## Changes Made

### File: `submit_to_tractor_ui.py`

**Updated Nuke executable path** (lines 547-550):
```python
# OLD:
nuke_exe = r"C:\Program Files\Nuke15.1v1\nuke.exe"

# NEW:
nuke_exe = r"C:\Program Files\Nuke15.1v2\Nuke15.1.exe"
```

**Added --nukex argument** (lines 552-557):
```python
# OLD:
cmd = [
    nuke_exe, "-x", script_path,
    "-F", f"{frame}-{frame}",
    "-X", write_name
]

# NEW:
cmd = [
    nuke_exe, "--nukex", "-x", script_path,
    "-F", f"{frame}-{frame}",
    "-X", write_name
]
```

## Expected Result
- Tractor jobs should now successfully execute on blades
- Blades will be able to find and run the correct Nuke executable
- Jobs will use NukeX mode as specified by the `--nukex` argument

## Testing
The changes have been applied and syntax validated. The next step is to:
1. Submit a test job through the Nuke UI
2. Monitor the job execution in Tractor
3. Verify that blades can successfully execute the Nuke commands

## File Status
- ✅ `submit_to_tractor_ui.py` - Updated with correct Nuke path and --nukex argument
- ✅ Syntax validation passed
- 🔄 Ready for testing with actual job submission

## Complete Command Format
Jobs will now execute with the following command structure:
```
"C:\Program Files\Nuke15.1v2\Nuke15.1.exe" --nukex -x [script_path] -F [frame_range] -X [write_name]
```

This should resolve the "program executable not found" errors and allow jobs to run successfully on the render farm.
