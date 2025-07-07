# UI Layout Reorganization and Job ID Fix

## Overview

The Tractor submission UI has been reorganized for better layout efficiency and the job ID URL encoding issue has been resolved.

## Changes Made

### 🎨 **UI Layout Reorganization**

#### ✅ **Before** (3-column layout)
```
┌─────────────┬─────────────┬─────────────┐
│ Write Nodes │   Job       │   Tractor   │
│             │ Settings    │   Monitor   │
│ [Refresh]   │             │             │
│             │ [Spool Job] │   [Link]    │
└─────────────┴─────────────┴─────────────┘
```

#### ✅ **After** (2-column layout)
```
┌─────────────┬─────────────┐
│ Write Nodes │   Job       │
│             │ Settings    │
│ [Refresh]   │             │
│             │             │
│ Tractor     │ [Spool Job] │
│ Monitor     │             │
│ [Link]      │             │
└─────────────┴─────────────┘
```

#### **Key Changes**
- **Removed**: Third column (right column)
- **Moved**: Tractor Job Monitor to bottom of left column
- **Simplified**: Two-column layout is more compact and efficient
- **Improved**: Better use of screen space

### 🔧 **Job ID URL Encoding Fix**

#### **Problem Identified**
- Job IDs containing curly braces (`{21540}`) were being URL encoded
- Resulted in malformed URLs like `http://10.31.240.8/tv/#jid=%7B21540%7D`
- Users saw "=%7B" instead of proper job ID

#### **Solution Implemented**
```python
# Clean and validate job ID 
job_id = str(result).strip()
# Remove any unwanted characters that might cause URL encoding issues
if '{' in job_id or '}' in job_id:
    print(f"[WARNING] Job ID contains curly braces: {job_id}")
    # Extract just the numeric part if possible
    import re
    numeric_match = re.search(r'\d+', job_id)
    if numeric_match:
        job_id = numeric_match.group()
        print(f"[DEBUG] Cleaned job ID: {job_id}")
```

#### **Job ID Cleaning Logic**
- **Input**: `{21540}` or `{'jid': 21540}` or similar problematic formats
- **Processing**: Extract numeric portion using regex
- **Output**: Clean job ID `21540`
- **Result**: Proper URL `http://10.31.240.8/tv/#jid=21540`

## Technical Details

### **Layout Changes**
```python
# Before: Three columns with separator
columns_layout = QtWidgets.QHBoxLayout()
├── left_column_layout (Write Nodes)
├── separator (Visual divider)  # ❌ REMOVED
├── right_column_layout (Job Settings)
├── separator (Visual divider)  # ❌ REMOVED
└── middle_column_layout (Tractor Monitor)  # ❌ REMOVED

# After: Two columns, Tractor Monitor in left column
columns_layout = QtWidgets.QHBoxLayout()
├── left_column_layout (Write Nodes + Tractor Monitor)
└── right_column_layout (Job Settings)
```

### **Job ID Cleaning**
```python
# Handles various problematic formats:
test_cases = [
    "21540",                    # ✅ Normal job ID
    "{21540}",                  # 🔧 Fixed: Extract 21540
    "jid:21540",               # 📝 Informational prefix
    " 21540 ",                 # 🔧 Fixed: Strip whitespace
    "{'jid': 21540}",          # 🔧 Fixed: Extract 21540
    "21540.0",                 # ✅ Decimal format (preserved)
    "21540abc",                # ⚠️  Mixed format (preserved)
]
```

## User Experience Improvements

### 🎯 **Better Layout**
- **More Compact**: Eliminates unnecessary third column
- **Logical Flow**: Tractor Monitor directly below Write Nodes
- **Screen Efficiency**: Better use of available space
- **Visual Balance**: Two-column layout is more harmonious

### 🔗 **Reliable Job Links**
- **Fixed URLs**: Job links now work correctly
- **Debug Output**: Clear logging when job IDs need cleaning
- **Robust Handling**: Handles various job ID formats automatically
- **User Feedback**: Debug messages show when cleaning occurs

### 📱 **Improved Workflow**
1. **Select Write Nodes** → Write nodes list with refresh button
2. **Monitor Access** → Tractor monitor link right below
3. **Configure Job** → Job settings in right column
4. **Submit Job** → Spool job button in job settings
5. **Direct Access** → Click job-specific links in success dialog

## Testing Results

### **Job ID Cleaning Test Results**
```
✅ Normal ID:     "21540"        → "21540"
🔧 Curly Braces: "{21540}"      → "21540" (cleaned)
📝 Prefix:       "jid:21540"    → "jid:21540" (preserved)
🔧 Whitespace:   " 21540 "      → "21540" (trimmed)
🔧 Dict Format:  "{'jid':21540}" → "21540" (cleaned)
✅ Decimal:      "21540.0"      → "21540.0" (preserved)
⚠️  Mixed:       "21540abc"     → "21540abc" (preserved)
```

### **URL Construction Test**
- **Before Fix**: `http://10.31.240.8/tv/#jid=%7B21540%7D` ❌
- **After Fix**: `http://10.31.240.8/tv/#jid=21540` ✅

## Benefits

### 🚀 **Performance**
- **Reduced Complexity**: Fewer UI elements to manage
- **Faster Rendering**: Simpler layout renders more quickly
- **Less Memory**: Fewer widgets in memory

### 👥 **User Experience**
- **Intuitive Layout**: Logical flow from top to bottom in left column
- **Working Links**: Job links now function correctly
- **Clean Interface**: No visual clutter from unnecessary columns
- **Immediate Access**: Tractor monitor easily accessible

### 🔧 **Maintenance**
- **Simpler Code**: Fewer layout elements to maintain
- **Robust URLs**: Automatic job ID cleaning prevents future issues
- **Better Debugging**: Clear logging when job IDs need processing
- **Future-Proof**: Handles various job ID formats automatically

The reorganized UI provides a cleaner, more efficient interface while ensuring that job monitoring links work reliably for all users.
