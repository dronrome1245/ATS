@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

set "TASK_ID=ATS2-M2-003"
set "TASK_NAME=Dataset manifest support"
set "REPORT_DIR=reports\local_ci"
set "REPORT=%REPORT_DIR%\CURRENT_TASK_REPORT.txt"
set "RC=0"

if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

> "%REPORT%" echo ATS CURRENT TASK REPORT
>> "%REPORT%" echo =======================
>> "%REPORT%" echo Task: %TASK_ID% - %TASK_NAME%
>> "%REPORT%" echo Started: %DATE% %TIME%
>> "%REPORT%" echo.

where git >nul 2>&1
if errorlevel 1 goto :git_missing

where uv >nul 2>&1
if errorlevel 1 goto :uv_missing

>> "%REPORT%" echo == tool versions ==
git --version >> "%REPORT%" 2>&1
uv --version >> "%REPORT%" 2>&1
>> "%REPORT%" echo.

echo [1/5] Updating repository...
>> "%REPORT%" echo == git pull --ff-only ==
git pull --ff-only >> "%REPORT%" 2>&1
if errorlevel 1 goto :pull_failed
>> "%REPORT%" echo.

for /f "delims=" %%H in ('git rev-parse HEAD 2^>nul') do set "HEAD_SHA=%%H"
>> "%REPORT%" echo Commit: %HEAD_SHA%
>> "%REPORT%" echo.

echo [2/5] Syncing frozen environment...
>> "%REPORT%" echo == uv sync --frozen ==
uv sync --frozen >> "%REPORT%" 2>&1
if errorlevel 1 goto :sync_failed
>> "%REPORT%" echo.

echo [3/5] Running current task tests...
>> "%REPORT%" echo == M2-003 Dataset Manifest tests ==
uv run --frozen python -m pytest tests/test_dataset_manifest.py -q >> "%REPORT%" 2>&1
if errorlevel 1 goto :task_tests_failed
>> "%REPORT%" echo.

echo [4/5] Running repository validator...
>> "%REPORT%" echo == repository validator ==
uv run --frozen python tools/validate_repo.py >> "%REPORT%" 2>&1
if errorlevel 1 goto :validator_failed
>> "%REPORT%" echo.

echo [5/5] Running full ATS Local CI...
>> "%REPORT%" echo == full local CI ==
uv run --frozen python tools/verify_repo.py >> "%REPORT%" 2>&1
if errorlevel 1 goto :full_gate_failed

>> "%REPORT%" echo.
>> "%REPORT%" echo ATS CURRENT TASK CHECK: PASS
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

:task_tests_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: current task tests failed.
set "RC=15"
goto :failed

:validator_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: repository validator failed.
set "RC=16"
goto :failed

:full_gate_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: full ATS Local CI failed.
set "RC=17"
goto :failed

:failed
>> "%REPORT%" echo ATS CURRENT TASK CHECK: FAIL
goto :finish

:finish
>> "%REPORT%" echo.
>> "%REPORT%" echo Finished: %DATE% %TIME%

echo.
type "%REPORT%"
echo.
echo ============================================================
echo Task: %TASK_ID%
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
