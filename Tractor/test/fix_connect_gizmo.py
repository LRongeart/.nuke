#!/usr/bin/env python
"""
Connect.gizmo Replacement Script
===============================

This script replaces Connect.gizmo nodes with Dot nodes to fix rendering issues.
Run this in Nuke's Script Editor before submitting to Tractor.
"""

import nuke

def replace_connect_with_dots():
    """Replace all Connect.gizmo nodes with Dot nodes to maintain connections"""
    
    # Find all nodes that might be Connect gizmos
    connect_nodes = []
    for node in nuke.allNodes():
        if 'Connect' in node.name() and ('gizmo' in node.Class().lower() or node.Class() == 'Group'):
            connect_nodes.append(node)
    
    print("Found {} Connect nodes to replace".format(len(connect_nodes)))
    
    replaced_count = 0
    for connect_node in connect_nodes:
        try:
            print("Replacing {}".format(connect_node.name()))
            
            # Get input connection
            input_node = connect_node.input(0) if connect_node.inputs() > 0 else None
            
            # Get all nodes that depend on this connect node
            output_nodes = connect_node.dependent()
            
            # Create a Dot node to replace the Connect
            dot = nuke.createNode('Dot', inpanel=False)
            dot.setName("Dot_{}".format(connect_node.name().replace('.', '_')))
            
            # Set position near the original node
            if hasattr(connect_node, 'xpos') and hasattr(connect_node, 'ypos'):
                dot.setXYpos(connect_node.xpos(), connect_node.ypos())
            
            # Connect the input
            if input_node:
                dot.setInput(0, input_node)
            
            # Reconnect all outputs
            for output_node in output_nodes:
                for i in range(output_node.inputs()):
                    if output_node.input(i) == connect_node:
                        output_node.setInput(i, dot)
            
            # Delete the original Connect node
            nuke.delete(connect_node)
            replaced_count += 1
            
        except Exception as e:
            print("Error replacing {}: {}".format(connect_node.name(), str(e)))
    
    print("Successfully replaced {} Connect nodes with Dot nodes".format(replaced_count))
    return replaced_count

def main():
    """Main function to run the replacement"""
    print("=" * 50)
    print("Connect.gizmo Replacement Tool")
    print("=" * 50)
    
    # Check if script is saved
    script_name = nuke.root().name()
    if script_name == "Root":
        print("WARNING: Script is not saved. Please save before running.")
        return False
    
    # Replace Connect nodes
    replaced = replace_connect_with_dots()
    
    if replaced > 0:
        # Save the modified script
        try:
            nuke.scriptSave()
            print("Script saved successfully with {} replacements".format(replaced))
            print("You can now submit this script to Tractor without Connect.gizmo errors.")
            return True
        except Exception as e:
            print("Error saving script: {}".format(str(e)))
            return False
    else:
        print("No Connect nodes found to replace.")
        return True

# Run the script if executed directly
if __name__ == "__main__":
    main()
