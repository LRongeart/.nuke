# Connect.gizmo Solution Script - CRITICAL ISSUE FIX

# URGENT: 16 Connect.gizmo nodes found causing render failures
# Error: "Connect.gizmo: unknown command" on render farm
# 
# This script can be run in Nuke to replace Connect.gizmo nodes with standard Nuke nodes before rendering.
#
# IMMEDIATE ACTION REQUIRED:
# 1. Open your Nuke script
# 2. Copy and paste the code below into Nuke's Script Editor
# 3. Run the script
# 4. Save your script  
# 5. Re-submit to Tractor

## Option 1: Replace Connect.gizmo with Dot nodes (safest)

```python
import nuke

def replace_connect_with_dots():
    """Replace all Connect.gizmo nodes with Dot nodes to maintain connections"""
    
    # Find all nodes that might be Connect gizmos
    connect_nodes = []
    for node in nuke.allNodes():
        if 'Connect' in node.name() and '.gizmo' in node.Class():
            connect_nodes.append(node)
        # Also check for Group nodes that might be Connect gizmos
        elif node.Class() == 'Group' and 'Connect' in node.name():
            connect_nodes.append(node)
    
    print(f"Found {len(connect_nodes)} Connect nodes to replace")
    
    for connect_node in connect_nodes:
        print(f"Replacing {connect_node.name()}")
        
        # Get input and output connections
        input_node = connect_node.input(0) if connect_node.inputs() > 0 else None
        output_nodes = connect_node.dependent()
        
        # Create a Dot node to replace the Connect
        dot = nuke.createNode('Dot', inpanel=False)
        dot.setName(f"Dot_{connect_node.name().replace('.', '_')}")
        
        # Set position near the original node
        if hasattr(connect_node, 'xpos') and hasattr(connect_node, 'ypos'):
            dot.setXYpos(connect_node.xpos(), connect_node.ypos())
        
        # Connect the input
        if input_node:
            dot.setInput(0, input_node)
        
        # Reconnect outputs
        for output_node in output_nodes:
            for i in range(output_node.inputs()):
                if output_node.input(i) == connect_node:
                    output_node.setInput(i, dot)
        
        # Delete the original Connect node
        nuke.delete(connect_node)
        
    print(f"Replaced {len(connect_nodes)} Connect nodes with Dot nodes")

# Run the replacement
replace_connect_with_dots()

# Save the script
nuke.scriptSave()
print("Script saved with Connect nodes replaced")
```

## Option 2: Create a simple Connect.gizmo replacement

```python
import nuke

def create_connect_gizmo():
    """Create a simple Connect.gizmo that just passes through the input"""
    
    # Create a group
    group = nuke.createNode('Group', inpanel=False)
    group.setName('Connect')
    
    # Enter the group
    group.begin()
    
    # Create Input and Output nodes
    input_node = nuke.createNode('Input', inpanel=False)
    output_node = nuke.createNode('Output', inpanel=False)
    
    # Connect them directly
    output_node.setInput(0, input_node)
    
    # Exit the group
    group.end()
    
    # Save as gizmo
    gizmo_path = "\\\\tls-storage02\\Install\\NUKE\\Nuke_PLUG\\.nuke\\Connect.gizmo"
    nuke.nodeCopy(gizmo_path)
    
    print(f"Created Connect.gizmo at {gizmo_path}")

# Uncomment to create the gizmo
# create_connect_gizmo()
```
