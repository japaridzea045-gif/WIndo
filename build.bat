@echo off
REM Builds Windo.exe. Needs Python 3.8+ installed (tick "Add to PATH").
REM Optional: put the Google "platform-tools" folder next to this file to bundle adb + fastboot.
pip install pyinstaller
REM remove old builds so you never run a stale Windo.exe
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q Windo.spec 2>nul
set HID=--hidden-import windo_db --hidden-import windo_games --hidden-import windo_apps --hidden-import windo_rules --hidden-import windo_boot
if exist platform-tools (
  pyinstaller --clean --onefile --windowed --name Windo %HID% --add-data "platform-tools;platform-tools" windo.py
) else (
  pyinstaller --clean --onefile --windowed --name Windo %HID% windo.py
)
echo.
echo Done. Your NEW app is in dist\Windo.exe  (run that one, not an older copy)
pause
