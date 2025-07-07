# Tractor Diagnostics Tools

These tools help diagnose why Tractor jobs are not being picked up by blades. They provide detailed analysis of blade capabilities, job requirements, and compatibility matching.

## Tools Overview

### 1. `tractor_diagnostics.py` - Full Diagnostics
**Purpose**: Comprehensive analysis of your Tractor farm
**What it does**:
- Connects to Tractor engine and queries all blades
- Analyzes blade capabilities (services, envkeys, crews, capacity)
- Reviews recent jobs to see what's working
- Tests multiple Nuke job configurations
- Provides detailed compatibility analysis and recommendations

**Usage**:
```bash
python tractor_diagnostics.py
```

### 2. `quick_job_test.py` - Quick Configuration Testing
**Purpose**: Fast testing of specific job configurations
**What it does**:
- Tests if a specific job configuration will be picked up
- Interactive mode for trying different settings
- Command-line mode for scripted testing

**Usage**:
```bash
# Interactive mode
python quick_job_test.py

# Command line mode
python quick_job_test.py NukeXRender rez ""
```

### 3. `run_diagnostics.bat` - Easy Windows Launcher
**Purpose**: One-click diagnostics on Windows
**What it does**:
- Sets up environment variables
- Runs full diagnostics
- Pauses to show results

**Usage**: Double-click the batch file

## Common Issues and Solutions

### Issue: "No blades are picking up jobs"

**Diagnostic Steps**:
1. Run `tractor_diagnostics.py` to get a full analysis
2. Check the "COMPATIBLE BLADES" section
3. Look at the "RECOMMENDATIONS" section

**Common Causes**:
- **Service mismatch**: Job requires "NukeXRender" but blades only have "NukeRender"
- **Envkey mismatch**: Job requires "rez" but blades don't have that environment
- **No active blades**: All blades are in "nimby" mode
- **No capacity**: Blades are busy with other jobs

### Issue: "Jobs are submitted but stay in queue"

**Check**:
- Job state (should be "ready", not "blocked" or "paused")
- Job priority (higher numbers = higher priority)
- Blade availability and capacity

### Issue: "Blades exist but don't match jobs"

**Solution**: Use the recommended configuration from diagnostics:
1. Run `tractor_diagnostics.py`
2. Look for "RECOMMENDED CONFIGURATION" 
3. Update your Nuke submission script with those settings

## Understanding Blade-Job Matching

Tractor matches jobs to blades based on:

1. **Service**: Job's service must match blade's available services
2. **Envkey**: Job's envkey must be available on the blade
3. **Crews**: Job's crews must match blade's crews (if specified)
4. **Capacity**: Blade must have available slots/capacity
5. **Priority**: Higher priority jobs get picked first

## Example Diagnostic Output

```
✅ COMPATIBLE BLADES:
  - blade01 (capacity: 2/4)
  - blade02 (capacity: 1/2)

❌ INCOMPATIBLE BLADES:
  - blade03:
    * Service mismatch: job needs 'NukeXRender', blade has ['NukeRender']
  - blade04:
    * No available capacity: 0/2

💡 RECOMMENDATIONS:
  - Job should be picked up by 2 compatible blade(s)
  - If job is still not picked up, check:
    * Job priority (higher priority jobs get picked up first)
    * Job state (should be 'ready' not 'blocked' or 'paused')
```

## Integration with Nuke UI

After running diagnostics, you can update your Nuke submission UI with the recommended settings:

1. **Service**: Use the service that most blades support
2. **Envkey**: Use envkeys that are available on active blades  
3. **Crews**: Use crew settings that match your blades (often empty)
4. **Priority**: Adjust based on your needs (500 is typical)

## Troubleshooting

### "Tractor API not available"
- Check that `TRACTOR_ENGINE` environment variable is set
- Verify Tractor installation and Python API availability
- Try: `set TRACTOR_ENGINE=simtracker:80`

### "Failed to connect to Tractor engine"
- Check network connectivity to simtracker
- Verify username/password in SIMTRACKER config
- Ensure Tractor engine is running

### "No blades found"
- Blades might be offline or in maintenance
- Check Tractor web interface for blade status
- Contact system administrator

## Advanced Usage

### Testing Custom Configurations
```python
from tractor_diagnostics import TractorDiagnostics

diag = TractorDiagnostics()
diag.connect_to_engine()
diag.query_all_blades()

# Test your specific config
config = {
    'service': 'MyCustomService',
    'envkey': ['custom_env'],
    'crews': ['rendering'],
    'owner': 'myuser',
    'priority': 750
}

compatible, incompatible = diag.analyze_job_blade_compatibility(config)
```

### Batch Testing Multiple Configs
```bash
# Test different services
python quick_job_test.py NukeXRender rez
python quick_job_test.py NukeRender rez  
python quick_job_test.py generic
```

This should help you quickly identify and fix blade matching issues!
