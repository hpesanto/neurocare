@echo off
REM ===========================================================================
REM NeuroCare Database Setup Script (Windows)
REM ===========================================================================
REM This script automates the PostgreSQL database setup for NeuroCare
REM
REM Requirements:
REM   - PostgreSQL installed and running
REM   - Python 3.8+ installed
REM   - Dependencies installed (pip install -r requirements.txt)
REM
REM Usage:
REM   1. Open Command Prompt or PowerShell
REM   2. Navigate to the NeuroCare project directory
REM   3. Run: setup_postgres.bat
REM ===========================================================================

setlocal enabledelayedexpansion

echo.
echo ==========================================================================
echo NeuroCare PostgreSQL Database Setup
echo ==========================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your PATH
    pause
    exit /b 1
)

REM Check if psycopg2 is available
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Warning: psycopg2 is not installed. Installing dependencies...
    python -m pip install -q -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install requirements
        pause
        exit /b 1
    )
)

REM Run the Python setup script
echo Running database setup...
echo.
python setup_postgres.py
set SETUP_RESULT=%errorlevel%

echo.
if %SETUP_RESULT% equ 0 (
    echo.
    echo ===========================================================================
    echo Setup completed successfully!
    echo ===========================================================================
    echo.
    echo Next steps:
    echo   1. Verify your database is running: psql -U postgres -h localhost
    echo   2. You can now start the Django development server:
    echo      python manage.py runserver
    echo.
) else (
    echo.
    echo Setup failed. Please check the errors above.
    echo.
)

pause
exit /b %SETUP_RESULT%
