@echo off
REM Fallback launcher if EMS-OS.exe has not been built: needs Python 3.10-3.12 already installed.
cd /d "%~dp0"
py -3 launcher\launcher.py || python launcher\launcher.py
