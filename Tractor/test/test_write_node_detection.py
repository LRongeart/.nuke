#!/usr/bin/env python
"""
Test script for enhanced Write node detection within Groups and Gizmos.
This script simulates the new find_all_write_nodes functionality.
"""

def simulate_nuke_environment():
    """Simulate a Nuke environment with Write nodes in various locations"""
    
    # Mock Nuke node structure
    class MockNode:
        def __init__(self, name, node_class, parent=None):
            self.node_name = name
            self.node_class = node_class
            self.parent = parent
            self.children = []
            self._disabled = False
            
        def name(self):
            return self.node_name
            
        def Class(self):
            return self.node_class
            
        def begin(self):
            print(f"    [ENTERING] {self.node_name} ({self.node_class})")
            
        def end(self):
            print(f"    [EXITING] {self.node_name} ({self.node_class})")
            
        def __getitem__(self, key):
            if key == 'disable':
                return MockKnob(self._disabled)
            return MockKnob(False)
    
    class MockKnob:
        def __init__(self, value):
            self._value = value
        def value(self):
            return self._value
    
    # Create mock node structure
    root_nodes = [
        MockNode("Write_Main", "Write"),
        MockNode("Write_Comp", "Write"),
        MockNode("Group_Effects", "Group"),
        MockNode("Gizmo_LensFlare", "Gizmo"),
        MockNode("Group_Color", "Group"),
    ]
    
    # Add Write nodes inside groups
    group_effects = root_nodes[2]
    group_effects.children = [
        MockNode("Write_Beauty", "Write", group_effects),
        MockNode("Write_Depth", "Write", group_effects),
        MockNode("Nested_Group", "Group", group_effects),
    ]
    
    # Add nested Write node
    nested_group = group_effects.children[2]
    nested_group.children = [
        MockNode("Write_AOV", "Write", nested_group),
    ]
    
    gizmo_lens = root_nodes[3]
    gizmo_lens.children = [
        MockNode("Write_Flare", "Write", gizmo_lens),
    ]
    
    group_color = root_nodes[4]
    group_color.children = [
        MockNode("Write_Grades", "Write", group_color),
        MockNode("Disabled_Write", "Write", group_color),
    ]
    # Disable one Write node
    group_color.children[1]._disabled = True
    
    return root_nodes

def test_write_node_detection(mock_nodes):
    """Test the enhanced Write node detection logic"""
    
    def find_all_write_nodes():
        """Simulated version of the enhanced Write node detection"""
        write_nodes = []
        
        def search_in_group(group_node, parent_path=""):
            """Recursively search for Write nodes inside a group"""
            group_node.begin()
            try:
                for node in group_node.children:
                    if node.Class() == 'Write':
                        # Create display name with parent group info
                        if parent_path:
                            display_name = f"{node.name()} ({parent_path} > {group_node.name()})"
                        else:
                            display_name = f"{node.name()} ({group_node.name()})"
                        
                        write_nodes.append({
                            'node': node,
                            'display_name': display_name,
                            'parent_group': group_node.name(),
                            'parent_path': parent_path,
                            'disabled': node['disable'].value()
                        })
                    
                    # Recursively search inside nested Groups and Gizmos
                    elif node.Class() in ['Group', 'Gizmo']:
                        nested_path = f"{parent_path} > {group_node.name()}" if parent_path else group_node.name()
                        search_in_group(node, nested_path)
            finally:
                group_node.end()
        
        # First, find all Write nodes at root level
        for node in mock_nodes:
            if node.Class() == 'Write':
                write_nodes.append({
                    'node': node,
                    'display_name': node.name(),
                    'parent_group': None,
                    'parent_path': None,
                    'disabled': node['disable'].value()
                })
        
        # Then search inside all Groups and Gizmos at root level
        for node in mock_nodes:
            if node.Class() in ['Group', 'Gizmo']:
                search_in_group(node)
        
        return write_nodes
    
    print("=" * 60)
    print("TESTING ENHANCED WRITE NODE DETECTION")
    print("=" * 60)
    
    # Test the detection
    write_nodes = find_all_write_nodes()
    
    print(f"\n🔍 Found {len(write_nodes)} Write nodes total:")
    print("-" * 40)
    
    enabled_count = 0
    for i, node_info in enumerate(write_nodes, 1):
        node = node_info['node']
        display_name = node_info['display_name']
        disabled = node_info['disabled']
        
        status = "❌ DISABLED" if disabled else "✅ ENABLED"
        print(f"{i:2d}. {display_name} {status}")
        
        if not disabled:
            enabled_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   • Total Write nodes found: {len(write_nodes)}")
    print(f"   • Enabled Write nodes: {enabled_count}")
    print(f"   • Disabled Write nodes: {len(write_nodes) - enabled_count}")
    
    print(f"\n📋 UI Display Examples:")
    print("   The following would appear in the Tractor UI Write nodes list:")
    for node_info in write_nodes:
        if not node_info['disabled']:
            print(f"   • {node_info['display_name']}")
    
    return write_nodes

if __name__ == "__main__":
    print("🎬 Simulating Nuke script with Write nodes in Groups and Gizmos...")
    
    # Create mock environment
    mock_nodes = simulate_nuke_environment()
    
    print(f"\n📁 Mock script structure:")
    for node in mock_nodes:
        print(f"   • {node.name()} ({node.Class()})")
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                print(f"     └── {child.name()} ({child.Class()})")
                if hasattr(child, 'children') and child.children:
                    for grandchild in child.children:
                        print(f"         └── {grandchild.name()} ({grandchild.Class()})")
    
    # Test the detection
    write_nodes = test_write_node_detection(mock_nodes)
    
    print(f"\n✅ Enhanced Write node detection test completed!")
