from cx_Freeze import setup, Executable
import sys

setup(
      name="game.exe",
      version="1.0",
      author="Sam Von Ehren",
      description="Copyright 2013",
      executables=[Executable(script = "main.py", base = "Win32GUI")],
      )
