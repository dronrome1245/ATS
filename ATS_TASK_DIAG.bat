@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
cd /d "%~dp0"

set "REPORT_DIR=reports\local_ci"
set "REPORT=%REPORT_DIR%\CURRENT_TASK_DIAG_REPORT.txt"
set "RC=0"

if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

> "%REPORT%" echo ATS CURRENT TASK DIAGNOSTIC REPORT
>> "%REPORT%" echo ==================================
>> "%REPORT%" echo Started: %DATE% %TIME%
>> "%REPORT%" echo Launcher: ATS_TASK_DIAG.bat
>> "%REPORT%" echo.

where uv >nul 2>&1
if errorlevel 1 goto :uv_missing

>> "%REPORT%" echo == uv sync --frozen ==
uv sync --frozen >> "%REPORT%" 2>&1
if errorlevel 1 goto :sync_failed
>> "%REPORT%" echo.

>> "%REPORT%" echo == current task diagnostic ==
uv run --frozen python tools/run_and_tee.py "%REPORT%" tools/current_task_diag.py %*
if errorlevel 1 goto :diag_failed

>> "%REPORT%" echo.
>> "%REPORT%" echo ATS TASK DIAGNOSTIC: COMPLETE
set "RC=0"
goto :finish

:uv_missing
>> "%REPORT%" echo ERROR: uv is not available on PATH.
set "RC=12"
goto :failed

:sync_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: uv sync --frozen failed.
set "RC=14"
goto :failed

:diag_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: current task diagnostic failed.
set "RC=15"
goto :failed

:failed
>> "%REPORT%" echo ATS TASK DIAGNOSTIC: FAIL
goto :finish

:finish
>> "%REPORT%" echo.
>> "%REPORT%" echo Finished: %DATE% %TIME%

echo.
echo ============================================================
echo Report file: %REPORT%
if "%RC%"=="0" (
  echo RESULT: COMPLETE
) else (
  echo RESULT: FAIL ^(exit code %RC%^)
)
echo ============================================================
echo.
echo Send reports\local_ci\CURRENT_TASK_DIAG_REPORT.txt to ChatGPT.
echo.
pause
exit /b %RC%
