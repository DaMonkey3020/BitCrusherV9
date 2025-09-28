@echo off
set "BC_PORTABLE=%~dp0"
set "PYTHONPATH=%BC_PORTABLE%\site\Lib\site-packages;%BC_PORTABLE%\app"
set "PATH=%BC_PORTABLE%\python;%BC_PORTABLE%\app\tools;%BC_PORTABLE%\tools;%PATH%"
set "TCL_LIBRARY=%BC_PORTABLE%\python\tcl\tcl8.6"
set "TK_LIBRARY=%BC_PORTABLE%\python\tcl\tk8.6"

