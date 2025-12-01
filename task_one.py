import shutil
import sys
from pathlib import Path


def get_args():
    """
    Call formats:
        python script.py source
        python script.py source destination
    If destination is not passed, 'dist' is used.
    """
    if len(sys.argv) < 2:
        print("Error: Specify the path to the output directory.")
        print("Example: python script.py C:\\input")
        sys.exit(1)

    source = Path(sys.argv[1])

    if len(sys.argv) >= 3:
        destination = Path(sys.argv[2])
    else:
        destination = Path("dist")

    return source, destination


def ensure_directory(path: Path):
    """
    Creates a directory if it does not exist.
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directory {path}: {e}")


def copy_file_to_ext_folder(file_path: Path, dest_root: Path):
    """
    Copies a file to a subdir named the file extension.
    Example:
        example.txt  →  dist/txt/example.txt
        image.jpeg   →  dist/jpeg/image.jpeg
        README       →  dist/no_extension/README
    """
    ext = file_path.suffix.lower().replace('.', '')

    # If there is no extension
    if not ext:
        ext = "no_extension"

    target_dir = dest_root / ext
    ensure_directory(target_dir)

    try:
        shutil.copy2(file_path, target_dir)
    except PermissionError:
        print(f"No access rights: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error while copying {file_path}: {e}")


def walk_directory_recursively(source_dir: Path, dest_root: Path):
    
    try:
        for entry in source_dir.iterdir():
            if entry.is_dir():
                walk_directory_recursively(entry, dest_root)
            elif entry.is_file():
                copy_file_to_ext_folder(entry, dest_root)
    except PermissionError:
        print(f"No access to directory: {source_dir}")
    except FileNotFoundError:
        print(f"Directory not found: {source_dir}")
    except Exception as e:
        print(f"Reading error {source_dir}: {e}")


def main():
    source, destination = get_args()

    if not source.exists() or not source.is_dir():
        print("Path does not exist or is not a directory.")
        sys.exit(1)

    ensure_directory(destination)

    walk_directory_recursively(source, destination)


if __name__ == "__main__":
    main()
