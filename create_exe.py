import os
import sys
import subprocess
import tkinter
import site

def get_tk_path():
    return os.path.dirname(tkinter.__file__)

def get_python_path():
    return sys.executable

def get_pyinstaller_path():
    possible_paths = [
        os.path.join(site.USER_SITE, "Scripts", "pyinstaller.exe"),
        os.path.join(site.USER_BASE, "Scripts", "pyinstaller.exe"),
        os.path.join(os.path.dirname(sys.executable), "Scripts", "pyinstaller.exe"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return "pyinstaller"

def create_exe():
    script_name = "r6_server_changer.py"
    tk_path = get_tk_path()
    tcl_path = os.path.join(tk_path, "tcl")
    tk_dll_path = os.path.join(tk_path, "tk")
    
    pyinstaller_path = get_pyinstaller_path()
    python_path = get_python_path()

    command = [
        python_path,
        pyinstaller_path,
        "--onefile",
        "--windowed",
        f"--add-data={tcl_path};tcl",
        f"--add-data={tk_dll_path};tk",
        script_name
    ]

    print("Executing command:", " ".join(command))
    
    try:
        subprocess.run(command, check=True)
        print(f"Executable created successfully. Check the 'dist' folder for {script_name.replace('.py', '.exe')}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Command output:")
        print(e.output)

if __name__ == "__main__":
    create_exe()