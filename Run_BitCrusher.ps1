$env:BC_PORTABLE = Split-Path -Parent $PSCommandPath
$env:PYTHONPATH = "$env:BC_PORTABLE\site\Lib\site-packages;$env:BC_PORTABLE\app"
$env:Path       = "$env:BC_PORTABLE\python;$env:BC_PORTABLE\app\tools;$env:BC_PORTABLE\tools;$env:Path"
$env:TCL_LIBRARY = "$env:BC_PORTABLE\python\tcl\tcl8.6"
$env:TK_LIBRARY  = "$env:BC_PORTABLE\python\tcl\tk8.6"
Set-Location "$env:BC_PORTABLE\app"
& "$env:BC_PORTABLE\python\python.exe" "BitCrusherV9.py"
