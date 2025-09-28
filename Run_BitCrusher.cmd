@echo off
setlocal
pushd "%~dp0"
call "%~dp0setenv.cmd"
pushd "%BC_PORTABLE%\app"
"%BC_PORTABLE%\python\python.exe" "BitCrusherV9.py"
set "EC=%ERRORLEVEL%"
popd
popd
endlocal & exit /b %EC%
