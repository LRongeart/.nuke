#!/usr/bin/env python
"""
Test Job ID URL Construction
Tests the job ID cleaning and URL construction for Tractor links
"""

import re

def clean_job_id(raw_result):
    """Clean and validate job ID from spool result"""
    job_id = str(raw_result).strip()
    
    # Remove any unwanted characters that might cause URL encoding issues
    if '{' in job_id or '}' in job_id:
        print(f"[WARNING] Job ID contains curly braces: {job_id}")
        # Extract just the numeric part if possible
        numeric_match = re.search(r'\d+', job_id)
        if numeric_match:
            job_id = numeric_match.group()
            print(f"[DEBUG] Cleaned job ID: {job_id}")
    
    return job_id

def test_url_construction():
    """Test URL construction with various job ID formats"""
    
    test_cases = [
        "21540",                    # Normal job ID
        "{21540}",                  # Job ID with curly braces (problematic)
        "jid:21540",               # Job ID with prefix
        " 21540 ",                 # Job ID with whitespace
        "{'jid': 21540}",          # Job ID as dict string
        "21540.0",                 # Job ID as float string
        "21540abc",                # Job ID with extra characters
    ]
    
    print("Testing Job ID Cleaning and URL Construction")
    print("=" * 50)
    
    for i, raw_result in enumerate(test_cases, 1):
        print(f"\nTest {i}: Raw result = '{raw_result}'")
        
        # Clean the job ID
        cleaned_id = clean_job_id(raw_result)
        print(f"  Cleaned ID: '{cleaned_id}'")
        
        # Construct URL
        tractor_url = f"http://10.31.240.8/tv/#jid={cleaned_id}"
        print(f"  Final URL: {tractor_url}")
        
        # Check for URL encoding issues
        if '{' in tractor_url or '}' in tractor_url or '%' in tractor_url:
            print(f"  ⚠️  WARNING: URL may have encoding issues")
        else:
            print(f"  ✅ URL looks clean")
    
    print("\n" + "=" * 50)
    print("EXPECTED BEHAVIOR:")
    print("- Raw result '21540' → URL: http://10.31.240.8/tv/#jid=21540")
    print("- Raw result '{21540}' → URL: http://10.31.240.8/tv/#jid=21540")
    print("- Raw result 'jid:21540' → URL: http://10.31.240.8/tv/#jid=21540")

def test_problematic_case():
    """Test the specific case that was causing issues"""
    print("\n" + "=" * 50)
    print("TESTING PROBLEMATIC CASE")
    print("=" * 50)
    
    # Simulate the case where URL showed "=%7B" instead of job ID
    problematic_result = "{21540}"  # This would URL encode { as %7B
    
    print(f"Problematic input: '{problematic_result}'")
    
    # Without cleaning
    bad_url = f"http://10.31.240.8/tv/#jid={problematic_result}"
    print(f"Without cleaning: {bad_url}")
    print(f"  This would URL encode to: http://10.31.240.8/tv/#jid=%7B21540%7D")
    
    # With cleaning
    cleaned_id = clean_job_id(problematic_result)
    good_url = f"http://10.31.240.8/tv/#jid={cleaned_id}"
    print(f"With cleaning: {good_url}")
    print(f"  ✅ This should work correctly!")

if __name__ == "__main__":
    test_url_construction()
    test_problematic_case()
