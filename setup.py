import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Rhythm",
        version = "0.1",
        description = "Our Own Music Player!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Rhythm.py", base=base)])