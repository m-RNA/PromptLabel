@echo off
setlocal
set "ROOT=%~dp0"
cd /d "%ROOT%"
set "PYTHON_EXE=%ROOT%.venv311\Scripts\python.exe"
set "MODEL_FILE=%ROOT%models\sam3.pt"
set "MAIN_FILE=%ROOT%main.py"
if not exist "%PYTHON_EXE%" (
    echo [ERROR] Missing venv python: %PYTHON_EXE%
    pause
    exit /b 1
)
if not exist "%MODEL_FILE%" (
    echo [ERROR] Missing model file: %MODEL_FILE%
    pause
    exit /b 1
)
start "" "%PYTHON_EXE%" "%MAIN_FILE%"
exit /b 0
