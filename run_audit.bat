@echo off
chcp 65001 >nul
title Repo Quality Guard
cls
echo ========================================================================
echo     REPO QUALITY GUARD — 1-Click Code Quality & Health Auditor
echo ========================================================================
echo.
echo   What do you want to test today?
echo.
echo   [1] QUICK AUDIT: Test current folder (Fast & Safe, Read-Only)
echo   [2] AUTO-FIX:    Test & automatically fix format errors (--fix)
echo   [3] MULTI-REPO:  Scan all projects in this workspace at once
echo   [4] CUSTOM:      Enter any specific folder path on your PC
echo   [5] TOOL DOCTOR: Check missing tools & install them interactively
echo   [6] EXIT
echo.
echo ========================================================================
echo.
set /p choice="Enter your choice [1-6]: "

if "%choice%"=="1" (
    echo.
    python "%~dp0repo_quality_guard.py" "%~dp0."
    goto done
)
if "%choice%"=="2" (
    echo.
    python "%~dp0repo_quality_guard.py" "%~dp0." --fix
    goto done
)
if "%choice%"=="3" (
    echo.
    python "%~dp0repo_quality_guard.py" "%~dp0." --all
    goto done
)
if "%choice%"=="4" (
    echo.
    set /p custom="Enter target folder path to test: "
    python "%~dp0repo_quality_guard.py" "%custom%"
    goto done
)
if "%choice%"=="5" (
    echo.
    python "%~dp0repo_quality_guard.py" --doctor
    goto done
)
if "%choice%"=="6" (
    exit /b 0
)

:done
echo.
echo Audit completed. Press any key to close...
pause >nul
