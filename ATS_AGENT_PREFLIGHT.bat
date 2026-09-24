@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
cd /d "%~dp0"

set "REPORT_DIR=reports\local_ci"
set "REPORT=%REPORT_DIR%\AGENT_PREFLIGHT_REPORT.txt"
set "RC=0"

if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

> "%REPORT%" echo ATS AGENT PREFLIGHT REPORT
>> "%REPORT%" echo ==========================
>> "%REPORT%" echo Started: %DATE% %TIME%
>> "%REPORT%" echo Launcher: ATS_AGENT_PREFLIGHT.bat
>> "%REPORT%" echo.

where git >nul 2>&1
if errorlevel 1 goto :git_missing

where uv >nul 2>&1
if errorlevel 1 goto :uv_missing

>> "%REPORT%" echo == git fetch origin main ==
git fetch origin main >> "%REPORT%" 2>&1
if errorlevel 1 goto :fetch_failed
>> "%REPORT%" echo.

>> "%REPORT%" echo == uv sync --frozen ==
uv sync --frozen >> "%REPORT%" 2>&1
if errorlevel 1 goto :sync_failed
>> "%REPORT%" echo.

>> "%REPORT%" echo == agent branch preflight ==
uv run --frozen python tools/run_and_tee.py "%REPORT%" tools/agent_preflight.py
if errorlevel 1 goto :preflight_failed

>> "%REPORT%" echo.
>> "%REPORT%" echo ATS AGENT PREFLIGHT: PASS
set "RC=0"
goto :finish

:git_missing
>> "%REPORT%" echo ERROR: git is not available on PATH.
set "RC=11"
goto :failed

:uv_missing
>> "%REPORT%" echo ERROR: uv is not available on PATH.
set "RC=12"
goto :failed

:fetch_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: git fetch origin main failed.
set "RC=13"
goto :failed

:sync_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: uv sync --frozen failed.
set "RC=14"
goto :failed

:preflight_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: agent branch preflight failed.
set "RC=15"
goto :failed

:failed
>> "%REPORT%" echo ATS AGENT PREFLIGHT: FAIL
goto :finish

:finish
>> "%REPORT%" echo.
>> "%REPORT%" echo Finished: %DATE% %TIME%

echo.
echo ============================================================
echo Report file: %REPORT%
if "%RC%"=="0" (
  echo RESULT: PASS
) else (
  echo RESULT: FAIL ^(exit code %RC%^)
)
echo ============================================================
echo.
echo Send reports\local_ci\AGENT_PREFLIGHT_REPORT.txt to ChatGPT.
echo.
pause
exit /b %RC%
