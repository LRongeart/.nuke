#!/usr/bin/env python
"""
Test Tractor Job URL Format
Validates the URL format for linking to specific jobs in Tractor web interface
"""

def test_tractor_job_urls():
    """Test various Tractor job URL formats"""
    
    base_url = "http://10.31.240.8/tv/"
    test_job_ids = [
        "12345",
        "67890", 
        "100001",
        "999999"
    ]
    
    print("Testing Tractor Job URL Formats")
    print("=" * 50)
    print(f"Base Tractor URL: {base_url}")
    print()
    
    # Common Tractor URL formats
    url_formats = [
        "{base_url}#jid={job_id}",           # Fragment-based (most common)
        "{base_url}?jid={job_id}",           # Query parameter
        "{base_url}job/{job_id}",            # Path-based
        "{base_url}jobs/{job_id}",           # Alternative path
        "{base_url}monitor/{job_id}",        # Monitor path
    ]
    
    print("Possible URL formats for job access:")
    for i, format_str in enumerate(url_formats, 1):
        print(f"\nFormat {i}: {format_str}")
        print("Examples:")
        for job_id in test_job_ids[:2]:  # Show 2 examples per format
            url = format_str.format(base_url=base_url, job_id=job_id)
            print(f"  Job {job_id}: {url}")
    
    print("\n" + "=" * 50)
    print("RECOMMENDATION:")
    print("The most common format for Pixar Tractor is:")
    print(f"{base_url}#jid={{job_id}}")
    print("\nThis uses URL fragments which allow direct navigation to specific jobs")
    print("without requiring server-side routing.")
    print("\n" + "=" * 50)

def generate_success_dialog_preview():
    """Generate a preview of what the success dialog will show"""
    
    print("\nSUCCESS DIALOG PREVIEW")
    print("=" * 50)
    
    # Mock submitted jobs
    submitted_jobs = [
        {'id': '12345', 'title': '[MyProject] scene.nk - Write1', 'write_node': 'Write1'},
        {'id': '12346', 'title': '[MyProject] scene.nk - Write2', 'write_node': 'Write2'},
    ]
    
    print("✅ Successfully submitted 2 job(s) to Tractor!")
    print()
    
    for job_info in submitted_jobs:
        job_id = job_info['id']
        write_node = job_info['write_node']
        tractor_url = f"http://10.31.240.8/tv/#jid={job_id}"
        
        print(f"📦 Job Container:")
        print(f"   Write Node: {write_node}")
        print(f"   🎬 View Job {job_id} in Tractor")
        print(f"   URL: {tractor_url}")
        print()
    
    print("─" * 30)
    print("🔗 Open Tractor Monitor (All Jobs)")
    print("URL: http://10.31.240.8/tv/")
    print()
    print("[Close Button]")

if __name__ == "__main__":
    test_tractor_job_urls()
    generate_success_dialog_preview()
