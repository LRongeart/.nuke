#!/usr/bin/env python
"""
Tractor EngineClient Method Discovery
====================================

This script discovers what methods are available on EngineClient
"""

import os
import sys

# Add local paths for Tractor API
script_dir = os.path.dirname(__file__)
tractor_path = os.path.join(script_dir, 'python2.7_portable', 'App', 'Python', 'Lib', 'site-packages')
if os.path.exists(tractor_path):
    sys.path.insert(0, tractor_path)

try:
    from tractor.base.EngineClient import EngineClient
    print("[SUCCESS] Tractor EngineClient imported")
    
    # Create an instance
    ec = EngineClient()
    print("[SUCCESS] EngineClient instance created")
    
    # Get all methods and attributes
    print("\n[DEBUG] Available methods and attributes:")
    methods = []
    for attr in dir(ec):
        if not attr.startswith('_'):
            attr_obj = getattr(ec, attr)
            attr_type = str(type(attr_obj))
            methods.append((attr, attr_type))
            print("  " + attr + " : " + attr_type)
    
    print("\n[DEBUG] Methods that look like query methods:")
    for name, attr_type in methods:
        if 'method' in attr_type and ('query' in name.lower() or 'get' in name.lower() or 'blade' in name.lower() or 'job' in name.lower()):
            print("  " + name + " : " + attr_type)
    
    # Test the spool method we know works
    print("\n[DEBUG] Testing spool method availability:")
    if hasattr(ec, 'spool'):
        print("  spool method is available!")
    else:
        print("  spool method NOT available!")
        
except Exception as e:
    print("[ERROR] Failed: " + str(e))
    import traceback
    traceback.print_exc()
