#!/usr/bin/env python
"""
Connect.gizmo Emergency Fix Script for Nuke

CRITICAL ISSUE: 16 Connect.gizmo nodes causing render failures
Error: "Connect.gizmo: unknown command" on render farm

IMMEDIATE SOLUTION:
1. Open your Nuke script that's failing to render
2. In Nuke, go to Window > Python Editor (or Script Editor)
3. Copy and paste this entire script
4. Click "Run" or press Ctrl+Enter
5. Save your script
6. Re-submit to Tractor

This script will automatically replace all Connect.gizmo nodes with Dot nodes,
preserving all connections while eliminating the render error.
"""

import nuke

def fix_connect_gizmo_emergency():
    """
    Emergency fix for Connect.gizmo render failures
    Replaces all Connect.gizmo nodes with Dot nodes
    """
    
    print("=" * 60)
    print("CONNECT.GIZMO EMERGENCY FIX")
    print("=" * 60)
    
    # Find all potential Connect gizmo nodes
    connect_nodes = []
    
    for node in nuke.allNodes():
        node_class = node.Class()
        node_name = node.name()
        
        # Check for Connect gizmos by class and name patterns
        if ('Connect' in node_class and 'gizmo' in node_class.lower()) or \
           ('Connect' in node_name and node_class == 'Group') or \
           node_class == 'Connect.gizmo':
            connect_nodes.append(node)
    
    if not connect_nodes:
        print("No Connect.gizmo nodes found. Script may already be fixed.")
        return
    
    print(f"FOUND {len(connect_nodes)} Connect.gizmo nodes to replace:")
    for node in connect_nodes:
        print(f"  - {node.name()} ({node.Class()})")
    
    # Replace each Connect node with a Dot node
    replaced_count = 0
    
    for connect_node in connect_nodes:
        try:
            print(f"\nReplacing {connect_node.name()}...")
            
            # Get position
            x_pos = connect_node.xpos()
            y_pos = connect_node.ypos()
            
            # Get input connection
            input_node = None
            if connect_node.inputs() > 0:
                input_node = connect_node.input(0)
            
            # Get output connections
            output_nodes = []
            for dep_node in nuke.allNodes():
                for i in range(dep_node.inputs()):
                    if dep_node.input(i) == connect_node:
                        output_nodes.append((dep_node, i))
            
            # Create replacement Dot node
            dot_node = nuke.nodes.Dot()
            dot_node.setXpos(x_pos)
            dot_node.setYpos(y_pos)
            dot_node.setName(f"Dot_{connect_node.name().replace('Connect', '')}")
            
            # Reconnect input
            if input_node:
                dot_node.setInput(0, input_node)
            
            # Reconnect outputs
            for output_node, input_index in output_nodes:
                output_node.setInput(input_index, dot_node)
            
            # Delete the Connect node
            nuke.delete(connect_node)
            
            print(f"  ✓ Replaced with {dot_node.name()}")
            replaced_count += 1
            
        except Exception as e:
            print(f"  ✗ Error replacing {connect_node.name()}: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"EMERGENCY FIX COMPLETE")
    print(f"Replaced {replaced_count} Connect.gizmo nodes with Dot nodes")
    print(f"=" * 60)
    print("\nNEXT STEPS:")
    print("1. Save your script (Ctrl+S)")
    print("2. Re-submit to Tractor")
    print("3. Monitor render logs for success")
    print("\nThis fix eliminates the 'Connect.gizmo: unknown command' error.")

# Run the emergency fix
if __name__ == "__main__":
    try:
        fix_connect_gizmo_emergency()
    except Exception as e:
        print(f"Emergency fix failed: {e}")
        print("Please contact pipeline support for manual assistance.")
