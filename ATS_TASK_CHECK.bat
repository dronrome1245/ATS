@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
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

echo Progress: [--------------------] 0%%
>> "%REPORT%" echo == git pull --ff-only ==
git pull --ff-only >> "%REPORT%" 2>&1
if errorlevel 1 goto :pull_failed
>> "%REPORT%" echo.
echo Progress: [##------------------] 10%%
>> "%REPORT%" echo == uv sync --frozen ==
uv sync --frozen >> "%REPORT%" 2>&1
if errorlevel 1 goto :sync_failed
>> "%REPORT%" echo.
echo Progress: [####----------------] 20%%
>> "%REPORT%" echo == fast local ci preflight ==
uv run --frozen python tools/verify_repo.py --fast >> "%REPORT%" 2>&1
if errorlevel 1 goto :preflight_failed
>> "%REPORT%" echo.
echo Progress: [########------------] 40%%
>> "%REPORT%" echo == current task check ==
uv run --frozen python tools/run_and_tee.py "%REPORT%" tools/current_task_check.py
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
>> "%REPORT%" echo Required ATS baseline: uv 0.12.13.
>> "%REPORT%" echo See governance\program\RESEARCH_ENVIRONMENT_SPEC.md and LOCAL_CI_TROUBLESHOOTING.md.
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

:preflight_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: fast Local CI preflight failed.
set "RC=16"
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
