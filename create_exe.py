import os
import sys
import subprocess
import tkinter

def get_tk_path():
    return os.path.dirname(tkinter.__file__)

def create_exe():
    script_name = "r6_server_changer.py"
    tk_path = get_tk_path()
    tcl_path = os.path.join(tk_path, "tcl")
    tk_dll_path = os.path.join(tk_path, "tk")

    command = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--add-data={tcl_path};tcl",
        f"--add-data={tk_dll_path};tk",
        script_name
    ]

    subprocess.run(command, check=True)

    print(f"Executable created successfully. Check the 'dist' folder for {script_name.replace('.py', '.exe')}")

if __name__ == "__main__":
    create_exe()