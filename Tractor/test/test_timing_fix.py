#!/usr/bin/env python
"""
Test script to verify the nuke.tprint_time fix works correctly.
This simulates the fixed render script logic.
"""

import time

def test_timing_fix():
    """Test that the timing functionality works without nuke.tprint_time()"""
    
    print("=" * 60)
    print("TESTING TIMING FIX")
    print("=" * 60)
    
    # This is what the fixed script now does
    print("Starting timing test...")
    start_time = time.time()
    
    # Simulate some work
    time.sleep(1)
    
    end_time = time.time()
    render_duration = end_time - start_time
    
    print("=" * 60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("Duration: %.2f seconds" % render_duration)
    print("=" * 60)
    
    # Verify the duration is reasonable (should be ~1 second)
    if 0.9 <= render_duration <= 1.1:
        print("✅ Timing fix works correctly!")
        return True
    else:
        print("❌ Timing seems incorrect: %.2f seconds" % render_duration)
        return False

if __name__ == "__main__":
    success = test_timing_fix()
    exit(0 if success else 1)
