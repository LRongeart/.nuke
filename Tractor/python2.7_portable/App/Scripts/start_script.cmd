@echo off
REM This script is automatically executed on console start
Title Portable Python 2.7.17 (64 bit) Console
REM PRINT python --version
python -c "import sys; print('Python' + sys.version)"
doskey pip=python -m pip $*
REM Add Scripts Path
SET PATH=%PYTHONPATH%\Scripts;%PATH%