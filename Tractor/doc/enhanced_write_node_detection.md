# Enhanced Write Node Detection - Documentation

## Overview
The Tractor submission UI now includes enhanced Write node detection that finds Write nodes not only at the root level of the Nuke script, but also inside Groups and Gizmos (including nested ones).

## Features

### 1. Recursive Detection
- **Root Level**: Detects all Write nodes at the script root level
- **Groups**: Searches inside all Group nodes for Write nodes  
- **Gizmos**: Searches inside all Gizmo nodes for Write nodes
- **Nested Groups**: Recursively searches inside nested Groups and Gizmos

### 2. Clear Display Names
Write nodes are displayed with their parent group information:
- **Root Write nodes**: `WriteNode1`
- **Inside Group**: `WriteNode1 (GroupName)`
- **Nested Groups**: `WriteNode1 (ParentGroup > ChildGroup)`
- **Inside Gizmo**: `WriteNode1 (GizmoName)`

### 3. Proper Node References
- Uses actual Nuke node references (stored in Qt item data)
- No longer dependent on node names for job submission
- Handles Write nodes with duplicate names in different groups

## Example UI Display

Before (root level only):
```
☐ Write_Main
☐ Write_Comp
```

After (enhanced detection):
```
☐ Write_Main
☐ Write_Comp
☐ Write_Beauty (Group_Effects)
☐ Write_Depth (Group_Effects)
☐ Write_AOV (Group_Effects > Nested_Group)
☐ Write_Flare (Gizmo_LensFlare)
☐ Write_Grades (Group_Color)
```

## Technical Implementation

### Key Methods
- `find_all_write_nodes()`: Main recursive search function
- `populateWriteNodes()`: Enhanced UI population method
- `search_in_group()`: Internal recursive helper function

### Data Structure
Each Write node is stored with:
```python
{
    'node': nuke_node_reference,
    'display_name': "WriteNode (GroupName)",
    'parent_group': "GroupName",
    'parent_path': "ParentGroup > ChildGroup"
}
```

### Safety Features
- **Context Management**: Properly enters/exits group contexts
- **Error Handling**: Graceful handling of missing or invalid nodes
- **State Preservation**: Always returns to original context after search
- **Disabled Node Filtering**: Only shows enabled Write nodes in UI

## Benefits

1. **Complete Coverage**: No more missed Write nodes hidden in groups
2. **Clear Organization**: Easy to identify which group contains each Write node
3. **Efficient Workflow**: Submit render jobs for Write nodes regardless of location
4. **Nested Support**: Handles arbitrarily deep group nesting
5. **Backward Compatible**: Still works with root-level Write nodes as before

## Usage
Simply click "Refresh Write Nodes" button and the UI will automatically detect and display all Write nodes in the script, regardless of their location within the node tree.

## Debug Output
When refreshing, the console will show:
```
[DEBUG] Found X Write nodes (including inside Groups/Gizmos)
```

This helps confirm that the enhanced detection is working and shows the total count of discovered Write nodes.
