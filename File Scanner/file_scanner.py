"""
File Scanning Engine
Recursively scans a directory and collects basic file metadata.
"""

from pathlib import Path
from datetime import datetime


def get_file_metadata(file_path):
    """Fetch metadata for a single file. Isolated so this can be swapped
    for a different source (e.g. Google Drive API) later."""
    try:
        stat = file_path.stat()
        return {
            "name": file_path.name,
            "path": str(file_path.resolve()),
            "size": stat.st_size,
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "last_accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
        }
    except (OSError, PermissionError):
        return None


def scan_directory(root_path):
    """Recursively scan root_path and return a list of file metadata dicts."""
    results = []
    root = Path(root_path)

    try:
        entries = root.rglob("*")
    except (OSError, PermissionError):
        return results

    for entry in entries:
        try:
            if not entry.is_file():
                continue
        except (OSError, PermissionError):
            continue

        metadata = get_file_metadata(entry)
        if metadata is not None:
            results.append(metadata)

    return results


if __name__ == "__main__":
    folder = input("Enter folder path to scan: ").strip()
    files = scan_directory(folder)

    print(f"\nScanned {len(files)} file(s).\n")
    for file_info in files[:5]:
        print(f"  Name:          {file_info['name']}")
        print(f"  Path:          {file_info['path']}")
        print(f"  Size:          {file_info['size']} bytes")
        print(f"  Last Modified: {file_info['last_modified']}")
        print(f"  Last Accessed: {file_info['last_accessed']}")
        print()
