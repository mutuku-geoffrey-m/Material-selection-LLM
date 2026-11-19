@echo off
REM Builds EMS-OS.exe in the project root. Run once on a Windows machine that has Python 3.10-3.12.
cd /d "%~dp0\.."
py -3 -m pip install --upgrade pyinstaller || goto :err
py -3 -m PyInstaller --onefile --console --name EMS-OS --distpath . --workpath build --specpath build launcher\launcher.py || goto :err
rmdir /s /q build 2>nul
echo.
echo Built EMS-OS.exe in the project root. Double-click it to run.
pause
exit /b 0
:err
echo Build failed.
pause
exit /b 1
