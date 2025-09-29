# Simple Connect.gizmo Test - Copy and paste this into Nuke Script Editor

import nuke

print("=== CONNECT.GIZMO TEST ===")

# Test 1: Try to create Connect node
try:
    connect_node = nuke.nodes.Connect()
    print("SUCCESS: Connect node created successfully!")
    print("Node class: " + connect_node.Class())
    print("Node name: " + connect_node.name())
    nuke.delete(connect_node)
    print("Connect.gizmo is working properly!")
except Exception as e:
    print("FAILED: Cannot create Connect node")
    print("Error: " + str(e))
    print("Connect.gizmo is not working")

# Test 2: Check if gizmo file exists
import os
gizmo_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke\nk_files\Connect.gizmo"
if os.path.exists(gizmo_path):
    print("Connect.gizmo file exists at: " + gizmo_path)
else:
    print("Connect.gizmo file NOT found at: " + gizmo_path)

print("=== TEST COMPLETE ===")
