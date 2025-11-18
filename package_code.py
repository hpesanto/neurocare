#!/usr/bin/env python3
"""
NeuroCare Code Package Script
==============================
This script packages the NeuroCare code for deployment.

Creates a ZIP file with all source code, excluding:
- Virtual environments
- __pycache__ directories
- .pyc files
- Git files (except .gitignore)
- Database files
- Large temporary files

Usage:
    python package_code.py
    python package_code.py --output ~/Downloads/neurocare.zip
"""

import os
import sys
import zipfile
import argparse
from pathlib import Path
from datetime import datetime

# Directories and files to exclude from the package
EXCLUDE_PATTERNS = {
    '__pycache__',
    '.venv',
    'venv',
    '.env',  # Never package .env with real credentials
    '*.pyc',
    '*.pyo',
    '.git',
    '.github',
    '.pytest_cache',
    'node_modules',
    'dist',
    'build',
    '*.egg-info',
    '.DS_Store',
    'Thumbs.db',
    '*.db',
    '*.sqlite3',
}

EXCLUDE_FILES = {
    '.env',  # Environment file with credentials
    'db.sqlite3',
    '.DS_Store',
    'Thumbs.db',
}


def should_exclude(path, relative_to):
    """Check if a path should be excluded from the package."""
    rel_path = path.relative_to(relative_to)
    
    # Check if any part of the path matches exclude patterns
    for part in rel_path.parts:
        if part in EXCLUDE_PATTERNS:
            return True
        
        # Check wildcard patterns
        for pattern in EXCLUDE_PATTERNS:
            if '*' in pattern:
                import fnmatch
                if fnmatch.fnmatch(part, pattern):
                    return True
    
    # Check filename
    if path.name in EXCLUDE_FILES:
        return True
    
    # Check filename patterns
    for pattern in EXCLUDE_PATTERNS:
        if '*' in pattern:
            import fnmatch
            if fnmatch.fnmatch(path.name, pattern):
                return True
    
    return False


def create_package(source_dir, output_file):
    """Create a ZIP package of the code."""
    
    source_path = Path(source_dir).resolve()
    output_path = Path(output_file).resolve()
    
    if not source_path.exists():
        print(f"❌ Error: Source directory not found: {source_path}")
        return False
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("NeuroCare Code Packaging")
    print("=" * 70)
    print(f"\nSource: {source_path}")
    print(f"Output: {output_path}")
    print()
    
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            total_size = 0
            
            print("📦 Scanning and packaging files...\n")
            
            for root, dirs, files in os.walk(source_path):
                # Remove excluded directories from dirs to prevent os.walk from traversing them
                dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d, source_path)]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    if should_exclude(file_path, source_path):
                        continue
                    
                    try:
                        # Calculate archive name (relative path)
                        arc_name = file_path.relative_to(source_path)
                        
                        # Add file to ZIP
                        zipf.write(file_path, arcname=arc_name)
                        
                        file_size = file_path.stat().st_size
                        total_size += file_size
                        file_count += 1
                        
                        # Show progress for larger files
                        if file_size > 1024 * 1024:  # Files larger than 1MB
                            size_mb = file_size / (1024 * 1024)
                            print(f"  ✓ {arc_name} ({size_mb:.2f} MB)")
                    
                    except Exception as e:
                        print(f"  ⚠️  Error adding {file_path}: {e}")
        
        # Print summary
        total_size_mb = total_size / (1024 * 1024)
        output_size_mb = output_path.stat().st_size / (1024 * 1024)
        
        print(f"\n✅ Package created successfully!")
        print(f"\n📊 Summary:")
        print(f"  Files packaged: {file_count}")
        print(f"  Total uncompressed size: {total_size_mb:.2f} MB")
        print(f"  Package size: {output_size_mb:.2f} MB")
        print(f"  Compression ratio: {(1 - output_size_mb / total_size_mb) * 100:.1f}%")
        print(f"\n📁 Location: {output_path}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error creating package: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Package NeuroCare code for deployment'
    )
    parser.add_argument(
        '--output',
        '-o',
        default=None,
        help='Output file path (default: ./neurocare_<date>.zip)'
    )
    parser.add_argument(
        '--source',
        '-s',
        default='.',
        help='Source directory (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Determine output file
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'neurocare_{timestamp}.zip'
    
    success = create_package(args.source, output_file)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
