#!/usr/bin/env python
"""
Test script to verify the enhanced job ID extraction logic.
"""

import json
import re

def extract_job_id(result):
    """New job ID extraction logic"""
    job_id = str(result).strip()
    print(f"[DEBUG] Raw job ID from spool: '{job_id}'")
    
    # Handle different result formats from Tractor
    actual_job_id = None
    
    # Check if result is a JSON string (new format)
    if job_id.startswith('{') and 'jid' in job_id:
        try:
            result_json = json.loads(job_id)
            if 'jid' in result_json:
                actual_job_id = str(result_json['jid'])
                print(f"[DEBUG] Extracted job ID from JSON: {actual_job_id}")
            elif 'msg' in result_json and 'jid:' in result_json['msg']:
                # Extract from message like "job script accepted, jid: 21545"
                match = re.search(r'jid:\s*(\d+)', result_json['msg'])
                if match:
                    actual_job_id = match.group(1)
                    print(f"[DEBUG] Extracted job ID from message: {actual_job_id}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[WARNING] Failed to parse JSON result: {e}")
    
    # If JSON parsing failed, try regex extraction on the raw string
    if actual_job_id is None:
        # Look for patterns like {jid:12345}, jid:12345, or just numbers
        jid_pattern = re.search(r'(?:jid[:=]\s*)?(\d+)', job_id)
        if jid_pattern:
            actual_job_id = jid_pattern.group(1)
            print(f"[DEBUG] Extracted job ID via regex: {actual_job_id}")
        else:
            # Final fallback - extract any numeric sequence
            numeric_match = re.search(r'\d+', job_id)
            if numeric_match:
                actual_job_id = numeric_match.group()
                print(f"[DEBUG] Fallback job ID extraction: {actual_job_id}")
    
    # Use the extracted job ID
    if actual_job_id:
        clean_job_id = actual_job_id
        print(f"[DEBUG] Final clean job ID: {clean_job_id}")
    else:
        # Use the original if extraction failed
        clean_job_id = job_id
        print(f"[WARNING] Could not extract numeric job ID, using raw: {clean_job_id}")
    
    return clean_job_id

def test_job_id_extraction():
    """Test various job ID formats"""
    
    test_cases = [
        # New JSON format from Tractor
        '{"rc": 0, "msg": "job script accepted, jid: 21545", "jid": 21545}',
        '{"jid": 21546, "status": "submitted"}',
        '{"rc": 0, "msg": "job script accepted, jid: 21547"}',
        
        # Old formats (for backward compatibility)
        '{21548}',
        'jid:21549',
        '21550',
        'Job 21551',
        
        # Edge cases
        '0',
        '',
        'error',
    ]
    
    print("=" * 60)
    print("TESTING JOB ID EXTRACTION")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_input}")
        print("-" * 40)
        try:
            extracted_id = extract_job_id(test_input)
            
            # Validate result
            if extracted_id and str(extracted_id).isdigit() and int(extracted_id) > 0:
                print(f"✅ SUCCESS: {extracted_id}")
            elif extracted_id == '0':
                print(f"⚠️  WARNING: Job ID is 0: {extracted_id}")
            else:
                print(f"❌ FAILED: Invalid job ID: {extracted_id}")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")

if __name__ == "__main__":
    test_job_id_extraction()
