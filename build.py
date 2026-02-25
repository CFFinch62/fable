import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

def print_step(msg):
    print(f"\n{'='*50}\n{msg}\n{'='*50}")

def get_version():
    # TODO: Extract version from fable/app.py or similar if possible.
    # For now, hardcoding based on About dialog info found in analysis.
    return "0.1.0"

def clean_build_artifacts():
    print_step("Cleaning previous build artifacts...")
    dirs_to_remove = ['build', 'dist', 'release']
    for d in dirs_to_remove:
        if os.path.exists(d):
            print(f"Removing {d}...")
            shutil.rmtree(d)
    
    spec_file = 'FABLE.spec'
    if os.path.exists(spec_file):
        print(f"Removing {spec_file}...")
        os.remove(spec_file)

def get_icon_path():
    system = platform.system()
    base_path = Path("images")
    if system == "Windows":
        return str(base_path / "fable.ico")
    elif system == "Darwin": # macOS
        return str(base_path / "fable.icns")
    else: # Linux and others
        # Use png for Linux if available, or fallback to the resource icon
        # The user's request implies using images folder, but it has no png
        # So we fall back to the one in resources for Linux window icon logic
        # But PyInstaller for Linux doesn't embed an icon in the elf executable the same way Windows does
        # It's mostly for the .desktop file or window icon. 
        # We will point to the png in resources for safety if images folder lacks png.
        # Actually, let's check if there is a png in images just in case
        if (base_path / "fable.png").exists():
             return str(base_path / "fable.png")
        return "fable/resources/icons/fable4-256.png"

def run_pyinstaller():
    print_step("Running PyInstaller...")
    
    system = platform.system()
    sep = os.pathsep
    
    # Basic command construction
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--windowed",
        "--name=FABLE",
        "--clean",
        # Include the entire fable package resources
        "--add-data=fable/resources:fable/resources",
    ]
    
    # Add icon if it exists
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        print(f"Using icon: {icon_path}")
        cmd.append(f"--icon={icon_path}")
    else:
        print(f"Warning: Icon not found at {icon_path}")

    # Hidden imports - PyQt6 usually handles itself, but sometimes plugins need help
    # Listing common ones just in case, though often not needed with modern PyInstaller hook
    # cmd.extend(["--hidden-import=PyQt6"]) 

    # Entry point
    cmd.append("fable.py")
    
    print(f"Executing: {' '.join(cmd)}")
    subprocess.check_call(cmd)

def create_release_package():
    print_step("Creating Release Package...")
    
    version = get_version()
    system = platform.system()
    machine = platform.machine()
    
    release_name = f"FABLE-{version}-{system}-{machine}"
    release_dir = Path("release") / release_name
    
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True)
    
    # Copy executable/bundle
    dist_dir = Path("dist")
    
    if system == "Darwin":
        # macOS creates a .app bundle
        src_app = dist_dir / "FABLE.app"
        if src_app.exists():
            shutil.copytree(src_app, release_dir / "FABLE.app")
        else:
            print("Error: FABLE.app not found in dist/")
            return
    else:
        # Windows/Linux create a directory (onedir mode is default)
        # Check if we are in onedir mode (default) or onefile. 
        # The command above didn't specify --onefile, so it used default (onedir)
        src_dir = dist_dir / "FABLE"
        if src_dir.exists():
             # Copy content of dist/FABLE into release_dir/FABLE
             # So the user gets a folder named FABLE inside the release zip
             shutil.copytree(src_dir, release_dir / "FABLE")
        else:
             print("Error: FABLE directory not found in dist/")
             return

    # Copy resource folders
    resources = ["docs", "examples", "libraries", "tutorial"]
    for res in resources:
        src = Path(res)
        dst = release_dir / res
        if src.exists():
            print(f"Copying {res}...")
            shutil.copytree(src, dst)
        else:
            print(f"Warning: Resource folder '{res}' not found.")

    # Create archive
    archive_format = "zip" if system == "Windows" else "gztar"
    archive_ext = "zip" if system == "Windows" else "tar.gz"
    
    archive_name = f"FABLE-{version}-{system}-{machine}"
    archive_path = Path("release") / archive_name
    
    print(f"Creating archive: {archive_path}.{archive_ext}")
    shutil.make_archive(str(archive_path), archive_format, "release", release_name)
    
    print_step(f"Build Success!\nRelease package created at: {archive_path}.{archive_ext}")

def main():
    try:
        clean_build_artifacts()
        run_pyinstaller()
        create_release_package()
    except subprocess.CalledProcessError as e:
        print_step("Build Failed during PyInstaller step.")
        sys.exit(1)
    except Exception as e:
        print_step(f"Build Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
