#!/usr/bin/env python
"""
Tractor Render Scripts Cleanup Utility

This script cleans up old temporary Python render scripts created by the Tractor submission system.
It looks for render scripts older than a specified number of days and removes them.

Usage:
- Run in Nuke Script Editor or from command line
- Customize the cleanup parameters below
"""

import os
import time
import glob

def cleanup_render_scripts(base_path=None, days_old=7, dry_run=False):
    """
    Clean up old render scripts from py/<script_name>/ directories.
    
    Args:
        base_path: Base path to search for py directories (default: current Nuke script directory)
        days_old: Remove scripts older than this many days (default: 7)
        dry_run: If True, only show what would be deleted without actually deleting
    """
    
    if base_path is None:
        try:
            import nuke
            current_script = nuke.scriptName()
            if current_script:
                base_path = os.path.dirname(current_script)
            else:
                print("No Nuke script open, please specify base_path")
                return
        except ImportError:
            print("Not running in Nuke, please specify base_path")
            return
    
    if not os.path.exists(base_path):
        print(f"Base path does not exist: {base_path}")
        return
    
    print("=" * 60)
    print("TRACTOR RENDER SCRIPTS CLEANUP")
    print("=" * 60)
    print(f"Base path: {base_path}")
    print(f"Days old threshold: {days_old}")
    print(f"Dry run: {dry_run}")
    print("=" * 60)
    
    # Find all py directories
    py_dirs = []
    for item in os.listdir(base_path):
        py_path = os.path.join(base_path, item)
        if os.path.isdir(py_path) and item == "py":
            py_dirs.append(py_path)
    
    if not py_dirs:
        print("No 'py' directories found")
        return
    
    total_deleted = 0
    total_size_deleted = 0
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)
    
    for py_dir in py_dirs:
        print(f"\nProcessing directory: {py_dir}")
        
        # Find all subdirectories (script name directories)
        for script_dir_name in os.listdir(py_dir):
            script_dir_path = os.path.join(py_dir, script_dir_name)
            if not os.path.isdir(script_dir_path):
                continue
                
            print(f"  Checking script directory: {script_dir_name}")
            
            # Find all render_*.py files in this directory
            render_files = glob.glob(os.path.join(script_dir_path, "render_*.py"))
            
            for render_file in render_files:
                try:
                    file_stat = os.stat(render_file)
                    file_age = file_stat.st_mtime
                    file_size = file_stat.st_size
                    
                    if file_age < cutoff_time:
                        age_days = (time.time() - file_age) / (24 * 60 * 60)
                        file_name = os.path.basename(render_file)
                        
                        if dry_run:
                            print(f"    [DRY RUN] Would delete: {file_name} (age: {age_days:.1f} days, size: {file_size} bytes)")
                        else:
                            os.remove(render_file)
                            print(f"    Deleted: {file_name} (age: {age_days:.1f} days, size: {file_size} bytes)")
                            
                        total_deleted += 1
                        total_size_deleted += file_size
                        
                except Exception as e:
                    print(f"    Error processing {render_file}: {e}")
            
            # Remove empty script directories
            try:
                if not dry_run and not os.listdir(script_dir_path):
                    os.rmdir(script_dir_path)
                    print(f"  Removed empty directory: {script_dir_name}")
            except Exception as e:
                print(f"  Could not remove directory {script_dir_name}: {e}")
    
    print("=" * 60)
    print("CLEANUP SUMMARY")
    print("=" * 60)
    if dry_run:
        print(f"Would delete: {total_deleted} files")
        print(f"Would free: {total_size_deleted} bytes ({total_size_deleted / 1024.0:.1f} KB)")
    else:
        print(f"Deleted: {total_deleted} files")
        print(f"Freed: {total_size_deleted} bytes ({total_size_deleted / 1024.0:.1f} KB)")
    print("=" * 60)

def cleanup_current_project(days_old=7, dry_run=False):
    """Cleanup render scripts for the current Nuke project."""
    cleanup_render_scripts(days_old=days_old, dry_run=dry_run)

def cleanup_all_projects(root_path, days_old=7, dry_run=False):
    """
    Cleanup render scripts for all projects under a root path.
    
    Args:
        root_path: Root path containing multiple project directories
        days_old: Remove scripts older than this many days
        dry_run: If True, only show what would be deleted
    """
    if not os.path.exists(root_path):
        print(f"Root path does not exist: {root_path}")
        return
    
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            cleanup_render_scripts(item_path, days_old, dry_run)

if __name__ == "__main__":
    # Example usage - customize these parameters
    
    # Cleanup current project (if running in Nuke)
    print("Cleaning up current project...")
    cleanup_current_project(days_old=7, dry_run=True)  # Set dry_run=False to actually delete
    
    # Or cleanup all projects under a specific path
    # print("Cleaning up all projects...")
    # cleanup_all_projects(r"\\tls-storage02\3D2\_NUKE", days_old=7, dry_run=True)
