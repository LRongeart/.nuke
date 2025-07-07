# IMPORTANT: TRACTOR API vs ALF FORMAT DIFFERENCES

## The Issue
The working .alf example shows task-level service, envkey, and refersto attributes:
```tcl
Task {Frame 1001} -service {"Denoise"} -envkey {} -refersto {"id0001"}
```

However, the Tractor Python API doesn't allow these attributes on Task objects - they're Job-level only.

## Python API Limitations Discovered:
1. **Task.service** ❌ - AttributeError: service is not a valid attribute of a Task
2. **Task.envkey** ❌ - AttributeError: envkey is not a valid attribute of a Task  
3. **Task.refersto** ❌ - AttributeError: refersto is not a valid attribute of a Task

## Valid Task Attributes (Python API):
✅ **Task.title** - Task name/description
✅ **Task.id** - Unique task identifier  
✅ **Task.argv** - Command to execute
✅ **Task.serialsubtasks** - Execution order control

## Valid Job Attributes (Python API):
✅ **Job.service** - Service for blade matching
✅ **Job.envkey** - Environment key for blade matching
✅ **Job.crews** - Crew restrictions
✅ **Job.projects** - Project associations

## The Solution
1. **Job-level attributes** (Python API): service, envkey, crews - handle blade matching
2. **Task-level attributes** (Python API): title, id, argv - handle execution
3. **TCL generation**: The Python API likely adds task-level service/envkey/refersto automatically when generating TCL

## Blade Query Fix:
The tq.blades() call requires a search clause:
```python
# ❌ Fails: blades = tq.blades()
# ✅ Works: blades = tq.blades(where=[["nimby", "=", "off"]])
```

## What this means:
- Our Job has the correct service (NukeXRender/NukeRender) and envkey
- Tasks have IDs for proper tracking
- The generated TCL should still include task-level services automatically
- Blade matching should work based on Job-level attributes

## Next steps:
1. Test job submission (should work now)
2. Check if jobs get picked up by blades  
3. Examine the generated TCL to see if task-level services appear
4. Use blade debugging to identify compatibility issues
