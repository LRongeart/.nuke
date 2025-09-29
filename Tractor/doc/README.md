# Tractor Nuke Integration

## Main Files

### Core Tractor Integration
- **`submit_to_tractor_ui.py`** - Main Tractor submission UI and job creation
- **`tractor_spool_bridge.py`** - Python 2.7 bridge for Tractor communication  
- **`submit_to_tractor.py`** - Legacy submission script (deprecated)

### Utilities
- **`cleanup_render_scripts.py`** - Cleanup old Python render scripts
- **`nuke_path_finder.py`** - Nuke executable detection utility

### Enhanced Plugin Loading
- **`enhanced_plugin_loading.py`** - Enhanced plugin loading for render farm
- **`enhanced_menu.py`** - Enhanced menu.py with Connect.gizmo fallbacks

## Directory Structure

```
tractor/
├── doc/                          # Documentation files
│   ├── ORGANIZED_RENDER_SCRIPTS.md
│   ├── CONNECT_GIZMO_LOADING_SOLUTION.md
│   └── ... (all other .md files)
├── test/                         # Test and diagnostic files  
│   ├── *test*.py
│   ├── *diagnostic*.py
│   ├── *FIX*.py
│   └── check_*.py
├── api/                          # Tractor API modules
├── packages/                     # Python packages
├── python2.7_portable/          # Portable Python 2.7
└── Main integration files (listed above)
```

## Usage

### Submit Render Job
```python
# In Nuke Script Editor
exec(open(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\submit_to_tractor_ui.py").read())
```

### Cleanup Old Scripts
```python
# In Nuke Script Editor  
exec(open(r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\cleanup_render_scripts.py").read())
cleanup_current_project(days_old=7, dry_run=False)
```

## Features

### ✅ Working Features
- **Robust job submission** with Python 2.7 bridge
- **Connect.gizmo loading** with multiple fallback methods
- **Organized Python render scripts** in `py/<script_name>/` folders
- **Automatic path resolution** respects existing Write node paths
- **Auto-directory creation** for output paths
- **Self-cleaning render scripts** after successful completion
- **Comprehensive error handling** and logging

### 🎯 Recent Improvements
- **Organized folder structure** - doc/, test/ folders created
- **Respects existing Write paths** - no forced "renders" folder
- **Auto-creates output directories** as needed
- **Enhanced logging** in render scripts
- **Cleanup utilities** for maintenance

## Documentation

All documentation has been moved to the `doc/` folder:
- Setup guides
- Troubleshooting
- API notes
- Feature explanations
- Historical analysis

## Testing

Test and diagnostic files are in the `test/` folder:
- Connection tests
- Path validation
- Plugin loading diagnostics
- Write node analysis
- Blade matching tests

## Maintenance

- **Cleanup render scripts**: Use `cleanup_render_scripts.py` regularly
- **Monitor py/ folders**: Check for accumulating render scripts
- **Review logs**: Check Tractor job logs for any issues
- **Update paths**: Verify network path accessibility from render farm
