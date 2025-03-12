import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    script_name = "r6_server_changer.py"
    output_name = "R6SiegeServerChanger"
    
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    command = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--name", output_name,
        "--onefile",
        "--windowed",
        "--noconsole",
        "--hidden-import", "tkinter",
        "--hidden-import", "json",
        "--icon", "r6_icon.ico" if os.path.exists("r6_icon.ico") else "NONE",
        script_name
    ]
    
    print(f"Building executable with command: {' '.join(command)}")
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        exe_path = Path("dist") / f"{output_name}.exe"
        print(f"✅ Build successful! Executable created at: {exe_path.absolute()}")
        print("\nNOTES:")
        print("1. If Windows Defender shows a warning, this is normal for PyInstaller executables")
        print("   You may need to add an exception or submit for Microsoft analysis")
        print("2. Distribute with r6_icon.ico in the same folder (if you're using an icon)")
    else:
        print(f"❌ Build failed with error code: {result.returncode}")
        print("Error output:")
        print(result.stderr)

if __name__ == "__main__":
    build_executable()