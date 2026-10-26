@echo off
chcp 65001 >nul
title Repo Quality Guard
echo ======================================================================
echo           REPO QUALITY GUARD — 6-IN-1 AUDIT SUITE
echo ======================================================================
echo.
echo [1] Run Health Audit on Current Directory
echo [2] Run Health Audit with Auto-Fix (--fix)
echo [3] Run Multi-Repo Batch Audit (--all)
echo [4] Audit Custom Path
echo [5] Tool Doctor & Setup Helper (Check & Install Missing Tools)
echo [6] Exit
echo.
set /p choice="Enter choice [1-6]: "

if "%choice%"=="1" (
    python "%~dp0repo_quality_guard.py" "%~dp0."
    goto done
)
if "%choice%"=="2" (
    python "%~dp0repo_quality_guard.py" "%~dp0." --fix
    goto done
)
if "%choice%"=="3" (
    python "%~dp0repo_quality_guard.py" "%~dp0." --all
    goto done
)
if "%choice%"=="4" (
    set /p custom="Enter target folder path: "
    python "%~dp0repo_quality_guard.py" "%custom%"
    goto done
)
if "%choice%"=="5" (
    python "%~dp0repo_quality_guard.py" --doctor
    goto done
)
if "%choice%"=="6" (
    exit /b 0
)

:done
echo.
pause
