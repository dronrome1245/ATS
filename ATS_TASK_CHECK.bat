@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

set "REPORT_DIR=reports\local_ci"
set "REPORT=%REPORT_DIR%\CURRENT_TASK_REPORT.txt"
set "RC=0"

if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

> "%REPORT%" echo ATS CURRENT TASK REPORT
>> "%REPORT%" echo =======================
>> "%REPORT%" echo Started: %DATE% %TIME%
>> "%REPORT%" echo Launcher: ATS_TASK_CHECK.bat
>> "%REPORT%" echo.

where git >nul 2>&1
if errorlevel 1 goto :git_missing

where uv >nul 2>&1
if errorlevel 1 goto :uv_missing

echo [1/3] Updating repository...
>> "%REPORT%" echo == git pull --ff-only ==
git pull --ff-only >> "%REPORT%" 2>&1
if errorlevel 1 goto :pull_failed
>> "%REPORT%" echo.

echo [2/3] Syncing frozen environment...
>> "%REPORT%" echo == uv sync --frozen ==
uv sync --frozen >> "%REPORT%" 2>&1
if errorlevel 1 goto :sync_failed
>> "%REPORT%" echo.

echo [3/3] Running current task check...
>> "%REPORT%" echo == current task check ==
uv run --frozen python tools/current_task_check.py >> "%REPORT%" 2>&1
if errorlevel 1 goto :task_failed

>> "%REPORT%" echo.
>> "%REPORT%" echo ATS TASK LAUNCHER: PASS
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

:pull_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: git pull --ff-only failed.
set "RC=13"
goto :failed

:sync_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: uv sync --frozen failed.
set "RC=14"
goto :failed

:task_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: current task check failed.
set "RC=15"
goto :failed

:failed
>> "%REPORT%" echo ATS TASK LAUNCHER: FAIL
goto :finish

:finish
>> "%REPORT%" echo.
>> "%REPORT%" echo Finished: %DATE% %TIME%

echo.
type "%REPORT%"
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
echo Send reports\local_ci\CURRENT_TASK_REPORT.txt to ChatGPT.
echo.
pause
exit /b %RC%
