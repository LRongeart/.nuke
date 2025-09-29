@echo off
echo Running Tractor Diagnostics...
echo ==============================

cd /d "\\tls-storage02\Install\NUKE\Nuke_PLUG\.nuke_DEV\tractor"

:: Set TRACTOR_ENGINE environment variable if not already set
if not defined TRACTOR_ENGINE (
    echo Setting TRACTOR_ENGINE...
    set TRACTOR_ENGINE=simtracker:80
)

echo TRACTOR_ENGINE is set to: %TRACTOR_ENGINE%
echo.

:: Run the diagnostics
python tractor_diagnostics.py

echo.
echo Diagnostics complete. Press any key to exit...
pause >nul
