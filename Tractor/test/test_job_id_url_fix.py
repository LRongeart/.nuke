#!/usr/bin/env python
"""
Test script to verify job ID URL encoding fix.
Tests the new job ID cleaning logic with various input formats.
"""

import re
import urllib.parse

def clean_job_id(raw_result):
    """New job ID cleaning logic from submit_to_tractor_ui.py"""
    job_id = str(raw_result).strip()
    print(f"[DEBUG] Raw job ID from spool: '{job_id}'")
    
    # Remove any unwanted characters that might cause URL encoding issues
    # Common patterns: {jid:12345}, jid:12345, or just 12345
    
    # First try to extract from patterns like {jid:12345} or jid:12345
    jid_pattern = re.search(r'(?:jid[:=]\s*)?(\d+)', job_id)
    if jid_pattern:
        clean_job_id = jid_pattern.group(1)
        print(f"[DEBUG] Extracted job ID: {clean_job_id}")
    else:
        # Fall back to extracting any numeric sequence
        numeric_match = re.search(r'\d+', job_id)
        if numeric_match:
            clean_job_id = numeric_match.group()
            print(f"[DEBUG] Fallback job ID extraction: {clean_job_id}")
        else:
            # Use the original if no numbers found (shouldn't happen)
            clean_job_id = job_id
            print(f"[WARNING] Could not extract numeric job ID, using raw: {clean_job_id}")
    
    return clean_job_id

def test_job_id_cleaning():
    """Test various job ID formats"""
    
    test_cases = [
        "{21540}",           # Your problematic case
        "jid:21541",         # Common Tractor format
        "{jid:21542}",       # Wrapped format
        "21543",             # Plain number
        "Job ID: 21544",     # With prefix
        "{Job 21545}",       # Complex format
        "some_text_21546_more",  # Embedded number
    ]
    
    print("=" * 60)
    print("TESTING JOB ID CLEANING AND URL GENERATION")
    print("=" * 60)
    
    for test_input in test_cases:
        print(f"\nInput: '{test_input}'")
        
        # Test old behavior (what would cause URL encoding issues)
        old_url = f"http://10.31.240.8/tv/#jid={test_input}"
        encoded_url = urllib.parse.quote(old_url, safe=':/?#')
        print(f"  Without cleaning: {old_url}")
        if '%' in encoded_url:
            print(f"  ❌ URL encoded problem: {encoded_url}")
        
        # Test new behavior
        cleaned_id = clean_job_id(test_input)
        new_url = f"http://10.31.240.8/tv/#jid={cleaned_id}"
        print(f"  With cleaning: {new_url}")
        print(f"  ✅ Clean job ID: {cleaned_id}")

if __name__ == "__main__":
    test_job_id_cleaning()
