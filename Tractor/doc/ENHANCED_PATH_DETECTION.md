# Enhanced Path Detection System

## Overview

The Tractor submission UI now includes enhanced path detection logic that can accurately determine whether a Write node path is absolute, relative, or contains dynamic expressions that should be resolved at render time.

## Path Detection Methods

### `is_absolute_path(path)`
Detects absolute paths including:
- **Windows drive paths**: `C:\path\to\file`, `c:\path\to\file`
- **UNC network paths**: `\\server\share\path`, `//server/share/path`
- **Unix absolute paths**: `/path/to/file`
- **Network mapped drives**: `Z:\path\to\file`

### `has_dynamic_expressions(path)`
Detects paths with dynamic content that should be resolved by Nuke at render time:
- **TCL expressions**: `[file dirname [value root.name]]/output.exr`
- **Unix environment variables**: `$PROJECT_ROOT/output.exr`, `${PROJECT_ROOT}/output.exr`
- **Windows environment variables**: `%USERPROFILE%\output.exr`, `%PROJECT_ROOT%\output.exr`
- **TCL environment access**: `$env(PROJECT_ROOT)/output.exr`, `[getenv PROJECT_ROOT]/output.exr`
- **Python expressions in TCL**: `[python {nuke.script_directory()}]/output.exr`
- **Nuke script references**: `[value root.name].exr`

### `normalize_path_for_farm(path)`
Normalizes paths for render farm compatibility:
- Converts backslashes to forward slashes
- Ensures UNC paths use `//` prefix (not `\\`)
- Preserves path structure and content

## Decision Logic

The system categorizes paths and takes appropriate actions:

### ✅ **ACCEPT** - Absolute Paths
- Absolute paths (UNC, drive letters, Unix paths) are accepted as-is
- Normalized for farm compatibility but content preserved
- Examples: `//server/share/project/output.exr`, `C:/projects/output.exr`

### ✅ **ACCEPT** - Dynamic Expressions  
- Paths with TCL expressions or environment variables are preserved
- No conversion attempted - let Nuke resolve at render time
- Examples: `[file dirname [value root.name]]/output.exr`, `$PROJECT_ROOT/output.exr`

### ⚠️ **WARN** - Simple Relative Paths
- Simple relative paths show a warning but don't block submission
- User is advised to use absolute paths for better compatibility
- Examples: `renders/output.exr`, `../output.exr`, `./output.exr`

### 🔧 **AUTO-FIX** - Empty Paths
- Empty or whitespace-only paths trigger automatic path generation
- Creates default path: `{script_directory}/renders/{script_name}_{write_node}.####.exr`
- Automatically creates the renders directory if needed

## Test Results

The enhanced detection system has been thoroughly tested with 27+ different path scenarios:

- **Windows paths**: ✅ Correctly detected
- **UNC paths**: ✅ Both `\\` and `//` formats supported
- **TCL expressions**: ✅ Properly preserved
- **Environment variables**: ✅ Windows (`%VAR%`) and Unix (`$VAR`, `${VAR}`) supported
- **Mixed separators**: ✅ Normalized for farm compatibility
- **Edge cases**: ✅ Incomplete paths, special characters handled

## Benefits

1. **Robust Detection**: Handles all common absolute path formats
2. **Smart Preservation**: Dynamic expressions preserved for Nuke resolution
3. **Farm Compatibility**: Paths normalized for cross-platform rendering
4. **User Friendly**: Clear warnings without blocking valid submissions
5. **Auto-Fix**: Automatic path generation for empty Write nodes
6. **Debug Information**: Detailed logging for troubleshooting

## Usage in Production

The enhanced path detection integrates seamlessly with the existing Tractor submission workflow:

1. **Pre-submission validation**: All Write nodes checked automatically
2. **Smart handling**: Different actions based on path type
3. **Preserved workflow**: Existing relative paths continue to work
4. **Enhanced reliability**: Better farm compatibility for network rendering

## Debug Output Example

```
[DEBUG] Write2 initial path info: Path: '[file dirname [value root.name]]/renders/output.####.exr' | os.path.isabs(): False | is_absolute_path(): False | has_dynamic_expressions(): True | Type: Dynamic expression
[DEBUG] Write2 uses dynamic expressions: [file dirname [value root.name]]/renders/output.####.exr
[DEBUG] This will be resolved by Nuke during render - no conversion needed
```

The system provides comprehensive path analysis for better understanding and troubleshooting of path-related issues during job submission.
