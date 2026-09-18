@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

set "REPORT_DIR=reports\local_ci"
set "REPORT=%REPORT_DIR%\LATEST_REPORT.txt"
set "RC=0"

if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

> "%REPORT%" echo ATS LOCAL CHECK REPORT
>> "%REPORT%" echo ======================
>> "%REPORT%" echo Started: %DATE% %TIME%
>> "%REPORT%" echo Launcher: ATS_CHECK.bat
>> "%REPORT%" echo.

where git >nul 2>&1
if errorlevel 1 goto :git_missing

where uv >nul 2>&1
if errorlevel 1 goto :uv_missing

>> "%REPORT%" echo == git version ==
git --version >> "%REPORT%" 2>&1
>> "%REPORT%" echo.

>> "%REPORT%" echo == uv version ==
uv --version >> "%REPORT%" 2>&1
>> "%REPORT%" echo.

echo [1/3] Updating repository...
>> "%REPORT%" echo == git pull --ff-only ==
git pull --ff-only >> "%REPORT%" 2>&1
if errorlevel 1 goto :pull_failed
>> "%REPORT%" echo.

for /f "delims=" %%H in ('git rev-parse HEAD 2^>nul') do set "HEAD_SHA=%%H"
>> "%REPORT%" echo Commit: %HEAD_SHA%
>> "%REPORT%" echo.

echo [2/3] Syncing frozen environment...
>> "%REPORT%" echo == uv sync --frozen ==
uv sync --frozen >> "%REPORT%" 2>&1
if errorlevel 1 goto :sync_failed
>> "%REPORT%" echo.

echo [3/3] Running full ATS Local CI...
>> "%REPORT%" echo == uv run --frozen python tools/verify_repo.py ==
uv run --frozen python tools/verify_repo.py >> "%REPORT%" 2>&1
if errorlevel 1 goto :verify_failed

>> "%REPORT%" echo.
>> "%REPORT%" echo ATS CHECK WRAPPER: PASS
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

:verify_failed
>> "%REPORT%" echo.
>> "%REPORT%" echo ERROR: ATS Local CI failed.
set "RC=15"
goto :failed

:failed
>> "%REPORT%" echo ATS CHECK WRAPPER: FAIL
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
echo Send reports\local_ci\LATEST_REPORT.txt to ChatGPT.
echo.
pause
exit /b %RC%
