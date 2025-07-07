# tractor_spool_bridge.py (Python 2)
import sys
import os

# Add Tractor API to sys.path for portable Python
tractor_api_path = os.path.join(
    os.path.dirname(__file__),
    'python2.7_portable', 'App', 'Python', 'Lib', 'site-packages'
)
sys.path.insert(0, tractor_api_path)

try:
    import json
except ImportError:
    import simplejson as json

from tractor.base.EngineClient import EngineClient



def main():
    try:
        # Read job data from stdin
        job_data = sys.stdin.read()
        print >>sys.stderr, "[BRIDGE DEBUG] Read %d bytes of job data" % len(job_data)
        
        # Get owner from command line argument, default to None
        owner = sys.argv[1] if len(sys.argv) > 1 else None
        print >>sys.stderr, "[BRIDGE DEBUG] Owner: %s" % owner
        
        # Get filename from command line argument, default to None
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        print >>sys.stderr, "[BRIDGE DEBUG] Filename: %s" % filename
        
        # Create EngineClient instance and spool the job
        print >>sys.stderr, "[BRIDGE DEBUG] Creating EngineClient..."
        ec = EngineClient()
        
        print >>sys.stderr, "[BRIDGE DEBUG] Spooling job..."
        result = ec.spool(job_data, owner=owner, filename=filename)
        
        print >>sys.stderr, "[BRIDGE DEBUG] Spool result type: %s" % type(result)
        print >>sys.stderr, "[BRIDGE DEBUG] Spool result repr: %s" % repr(result)
        print >>sys.stderr, "[BRIDGE DEBUG] Spool result: %s" % result
        
        # Print result as JSON for easy parsing in Python 3
        print(json.dumps({"result": result}))
        
    except Exception as e:
        print >>sys.stderr, "[BRIDGE ERROR] Exception occurred: %s" % str(e)
        import traceback
        print >>sys.stderr, "[BRIDGE ERROR] Traceback: %s" % traceback.format_exc()
        # Return error result
        print(json.dumps({"result": 0, "error": str(e)}))
    

if __name__ == '__main__':
    main()