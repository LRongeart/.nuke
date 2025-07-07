# KEY FIXES BASED ON WORKING EXAMPLE

## Comparison: Our Job vs Working Denoise Job

### BEFORE (Our original job):
```tcl
Job -title {...} -projects {{EXIT}} -service {NukeXRender} -envkey {{nukex-15.1}} -crews {{3D4}} -maxactive 10 -tier {windows} -minslots 1 -maxslots 1 -serialsubtasks 0 -subtasks {
  Task {Render Write2} -subtasks {
    Task {Frame 1} -cmds {
      RemoteCmd {{nuke.exe} {-x} {...}}
    }
  }
}
```

### AFTER (Matching working example):
```tcl
Job -title {...} -project {EXIT} -service {PixarRender} -envkey {} -crews {{3D4}} -maxactive {0} -serialsubtasks 1 -subtasks {
  Task {Render Write2} -serialsubtasks 0 -subtasks {
    Task {Frame 1} -id {id0001} -service {Nuke} -envkey {} -refersto {id0001} -cmds {
      RemoteCmd {{nuke.exe} {-x} {...}}
    }
  }
}
```

## Key Changes Made:

1. **Job Service**: Changed from `NukeXRender` to `PixarRender` (matches working example)
2. **Envkey**: Changed from specific `nukex-15.1` to empty `{}` (matches working example) 
3. **Project**: Changed from `projects` (array) to `project` (single value)
4. **MaxActive**: Changed from `10` to `0` (unlimited, matches working example)
5. **SerialSubtasks**: Added at job level with value `1`
6. **Task Attributes**: Added task-level `service`, `envkey`, `id`, and `refersto`
7. **Removed Attributes**: Removed `tier`, `minslots`, `maxslots` (not in working example)

## Why These Changes Should Fix Blade Matching:

- **PixarRender**: This appears to be the main render service your farm uses
- **Empty Envkey**: Matches any environment, more flexible than specific versions
- **Task-level Service**: "Nuke" is simpler and likely what blades advertise
- **Proper IDs**: Allows Tractor to properly track task dependencies
- **Unlimited MaxActive**: Allows more parallel execution

## Next Steps:

1. Test with "PixarRender" service and empty envkey
2. If still not working, use the "Debug: Show Available Blades" button to see exact services
3. Try the test_blade_matching.py script to find the perfect combination
