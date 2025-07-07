# Nuke Path Resolution Guide

## Automatic Path Resolution Options

### 1. **Automatic Script-Relative Resolution** ✅ IMPLEMENTED
The system now automatically converts relative paths to absolute paths based on the script location.

**Example:**
- Script location: `//tls-storage02/3D2/_NUKE/project/script.nk`
- Write path: `OUT/render.####.exr`
- **Auto-resolved to:** `//tls-storage02/3D2/_NUKE/project/OUT/render.####.exr`

**How it works:**
```python
# The system automatically:
script_dir = os.path.dirname(script_path)
absolute_path = os.path.join(script_dir, relative_path)
write_node['file'].setValue(absolute_path)
```

### 2. **TCL Expression Support** ✅ SUPPORTED

**Common TCL expressions that work:**
```tcl
# Project root variable
[value root.project_directory]/OUT/render.####.exr

# Script name variable  
[file dirname [value root.name]]/OUT/[file rootname [file tail [value root.name]]].####.exr

# Environment variables
$NUKE_TEMP_DIR/render.####.exr

# Relative with TCL
[file dirname [value root.name]]/../RENDER/output.####.exr
```

**Advantages of TCL paths:**
- ✅ Automatically resolve at render time
- ✅ Portable between different environments  
- ✅ Can use Nuke's built-in variables
- ✅ Handle complex path logic

### 3. **Manual Absolute Paths** ✅ ALWAYS WORKS
```
//tls-storage02/3D2/_NUKE/project/OUT/render.####.exr
\\tls-storage02\3D2\_NUKE\project\OUT\render.####.exr
```

## Recommended Path Patterns

### **For Your Setup:**

#### **Option A: TCL-Based (Recommended)**
```tcl
[file dirname [value root.name]]/OUT/[file rootname [file tail [value root.name]]].####.exr
```
This creates: `script_directory/OUT/script_name.####.exr`

#### **Option B: Project-Relative with TCL**
```tcl
[value root.project_directory]/RENDER/[file rootname [file tail [value root.name]]]/v001/####.exr
```

#### **Option C: Simple Relative (Auto-Resolved)**
```
OUT/render.####.exr
```
The system will automatically convert this to an absolute path.

## Path Resolution Priority

1. **Direct absolute path** → Used as-is
2. **TCL expressions** → Resolved by Nuke at render time
3. **`write_node.filename()`** → Nuke's evaluated path
4. **Auto-conversion** → Script-directory + relative path
5. **Warning + Continue** → For remaining relative paths

## Testing Your Setup

### **Test TCL Expression:**
```python
# In Nuke console:
write_node = nuke.toNode('Write2')
print("Raw path:", write_node['file'].value())
print("Evaluated path:", write_node.filename())

# Test TCL evaluation:
test_expr = "[file dirname [value root.name]]/OUT/test.exr"
result = nuke.tcl("return " + test_expr)
print("TCL result:", result)
```

### **Verify Auto-Resolution:**
The submission system will show debug output like:
```
[DEBUG] Converted relative path 'OUT/render.exr' to absolute: '//tls-storage02/3D2/_NUKE/project/OUT/render.exr'
[DEBUG] Updated Write node 'Write2' with absolute path
```

## Best Practices

### **For Render Farm Compatibility:**
1. **Use forward slashes** in network paths: `//server/path/file.exr`
2. **Include frame padding**: `####` or `%04d`
3. **Use EXR format** for reliability
4. **Test locally first** before submitting to farm

### **Recommended Write Node Setup:**
```tcl
# File path:
[file dirname [value root.name]]/OUT/[file rootname [file tail [value root.name]]].####.exr

# This automatically creates:
# //tls-storage02/3D2/_NUKE/project/OUT/script_name.0001.exr
```

**Your current case:**
- Path: `OUT/RebuildEnvironment_COM_v001.exr`  
- **Will become:** `//tls-storage02/3D2/_NUKE/3D2_NUKE_010_CG/ESMA_10_3D3_RebuildEnvironment/OUT/RebuildEnvironment_COM_v001.exr`

The automatic resolution should solve your current render issue!
