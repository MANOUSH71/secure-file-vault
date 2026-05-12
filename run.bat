@echo off
echo ========================================
echo  Secure File Vault Pro - Web App
echo ========================================
echo.

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/3] Installing requirements...
pip install -r requirements.txt

echo.
echo [3/3] Starting application...
echo.
echo ========================================
echo  Application running at:
echo  http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
