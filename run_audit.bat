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
echo [5] Exit
echo.
set /p choice="Enter choice [1-5]: "

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
    exit /b 0
)

:done
echo.
pause
