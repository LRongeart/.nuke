# UPDATED CHANGES BASED ON YOUR REQUIREMENTS

## What we kept from the working example structure:
✅ **Task IDs and refersto** - For proper Tractor task tracking  
✅ **Empty envkey** - For maximum blade compatibility  
✅ **Task-level service attributes** - Following the working pattern  
✅ **Removed problematic attributes** - No more tier/minslots/maxslots  

## What we customized for your Nuke workflow:

### 1. Services:
- **Job-level**: `NukeXRender` or `NukeRender` (your choice)
- **Task-level**: Same as job-level service (both levels match)

### 2. Envkey:
- **Default**: Empty (leave blank for maximum compatibility)
- **Override**: Manual field to enter specific envkey if needed

### 3. Projects:
- **Format**: Kept as `projects` array (not singular `project`)
- **Reason**: You need to select between different projects

### 4. Max Active Tasks:
- **UI**: Added spinner control (0-999)
- **Default**: 10 tasks
- **Special**: 0 = "Unlimited"

### 5. SerialSubtasks:
- **Job level**: Set to 1 (tasks execute in order)
- **Master task**: Set to 0 (frames can run in parallel)
- **Purpose**: Controls execution order - 1=sequential, 0=parallel

## About SerialSubtasks:
```
serialsubtasks = 1: Tasks must complete before next starts (A→B→C)
serialsubtasks = 0: Tasks can run simultaneously (A+B+C)
```

For rendering:
- Job level = 1: Write nodes render one at a time
- Frame level = 0: Frames within a write node can render in parallel

## Current Structure:
```tcl
Job -service {NukeXRender} -envkey {} -maxactive 10 -serialsubtasks 1 -subtasks {
  Task {Render Write1} -serialsubtasks 0 -subtasks {
    Task {Frame 1} -id {id0001} -service {NukeXRender} -envkey {} -refersto {id0001}
    Task {Frame 2} -id {id0002} -service {NukeXRender} -envkey {} -refersto {id0002}
  }
}
```

This should now match your requirements while keeping the structural improvements from the working example!
