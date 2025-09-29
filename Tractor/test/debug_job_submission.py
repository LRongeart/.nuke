#!/usr/bin/env python
"""
Test script to debug Tractor job submission issues.
This script helps identify why job IDs are being returned as 0.
"""

import sys
import os
import subprocess
import json

def test_bridge_connection():
    """Test the Python 2.7 bridge connection"""
    
    python2_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\python2.7_portable\App\Python\python.exe"
    bridge_script = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\tractor_spool_bridge.py"
    
    print("=" * 60)
    print("TESTING TRACTOR BRIDGE CONNECTION")
    print("=" * 60)
    
    # Check if files exist
    print(f"🔍 Checking Python 2.7 path: {python2_path}")
    if os.path.exists(python2_path):
        print("✅ Python 2.7 executable found")
    else:
        print("❌ Python 2.7 executable NOT found")
        return False
    
    print(f"🔍 Checking bridge script: {bridge_script}")
    if os.path.exists(bridge_script):
        print("✅ Bridge script found")
    else:
        print("❌ Bridge script NOT found")
        return False
    
    # Test basic bridge execution
    print(f"🔍 Testing bridge execution...")
    try:
        # Create a minimal test job TCL
        test_job_tcl = '''Job -title "Test Job" -priority 100 -service "PixarRender" {
    Task -title "Test Task" {
        Cmd {echo "Hello World"}
    }
}'''
        
        cmd_args = [python2_path, bridge_script, "test_user", "test.nk"]
        
        print(f"Command: {' '.join(cmd_args)}")
        print(f"Job TCL length: {len(test_job_tcl)} bytes")
        
        proc = subprocess.Popen(
            cmd_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        out, err = proc.communicate(input=test_job_tcl.encode('utf-8'))
        
        print(f"Return code: {proc.returncode}")
        print(f"Stdout: {out.decode('utf-8')}")
        print(f"Stderr: {err.decode('utf-8')}")
        
        if proc.returncode == 0:
            try:
                result = json.loads(out.decode('utf-8'))
                job_id = result.get("result", "NO_RESULT")
                error = result.get("error", None)
                
                print(f"✅ Bridge executed successfully")
                print(f"📊 Result: {job_id}")
                print(f"📊 Error: {error}")
                
                if job_id == 0 or job_id == "0":
                    print("⚠️  WARNING: Job ID is 0 - this indicates a Tractor issue")
                    print("   Possible causes:")
                    print("   • Tractor engine is not running")
                    print("   • Authentication issues")
                    print("   • Job validation errors")
                    print("   • Network connectivity problems")
                elif job_id and str(job_id).isdigit() and int(job_id) > 0:
                    print(f"🎉 SUCCESS: Valid job ID received: {job_id}")
                else:
                    print(f"❓ UNCLEAR: Unexpected job ID format: {job_id}")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON output: {e}")
                return False
        else:
            print(f"❌ Bridge execution failed with code {proc.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during bridge test: {e}")
        return False

def test_tractor_connectivity():
    """Test direct connectivity to Tractor engine"""
    
    print("\n" + "=" * 60)
    print("TESTING DIRECT TRACTOR CONNECTIVITY")
    print("=" * 60)
    
    try:
        # Try to import Tractor modules through the bridge
        python2_path = r"\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor\python2.7_portable\App\Python\python.exe"
        
        test_script = '''
import sys
import os

# Add Tractor API to sys.path
tractor_api_path = os.path.join(
    os.path.dirname(__file__),
    'python2.7_portable', 'App', 'Python', 'Lib', 'site-packages'
)
sys.path.insert(0, tractor_api_path)

try:
    from tractor.base.EngineClient import EngineClient
    print("SUCCESS: Tractor modules imported")
    
    ec = EngineClient()
    print("SUCCESS: EngineClient created")
    
    # Try to get engine status
    # Note: This might fail if Tractor engine is not running
    
except Exception as e:
    print("ERROR: %s" % str(e))
    import traceback
    traceback.print_exc()
'''
        
        with open("temp_tractor_test.py", "w") as f:
            f.write(test_script)
        
        proc = subprocess.Popen(
            [python2_path, "temp_tractor_test.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(python2_path)
        )
        
        out, err = proc.communicate()
        
        print(f"Test output: {out.decode('utf-8')}")
        print(f"Test errors: {err.decode('utf-8')}")
        
        # Clean up
        if os.path.exists("temp_tractor_test.py"):
            os.remove("temp_tractor_test.py")
        
        if "SUCCESS: EngineClient created" in out.decode('utf-8'):
            print("✅ Tractor connectivity test passed")
            return True
        else:
            print("❌ Tractor connectivity test failed")
            return False
            
    except Exception as e:
        print(f"❌ Exception during connectivity test: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Tractor Job Submission Debugging Tool")
    print("This tool helps diagnose why job IDs are being returned as 0")
    
    bridge_ok = test_bridge_connection()
    tractor_ok = test_tractor_connectivity()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Bridge Connection: {'✅ OK' if bridge_ok else '❌ FAILED'}")
    print(f"Tractor Connectivity: {'✅ OK' if tractor_ok else '❌ FAILED'}")
    
    if not bridge_ok:
        print("\n🚨 Bridge connection failed - check Python 2.7 installation")
    elif not tractor_ok:
        print("\n🚨 Tractor connectivity failed - check Tractor engine status")
    else:
        print("\n🎉 All tests passed - the issue might be in the job TCL or Tractor configuration")
    
    print("\n💡 Next steps:")
    print("1. Check if Tractor engine is running: http://10.31.240.8/tv/")
    print("2. Verify Tractor user credentials")
    print("3. Check Tractor engine logs for submission errors")
    print("4. Ensure proper network connectivity to Tractor server")
