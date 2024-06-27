@echo off
:: relaunch app with minimized command prompt
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && cmd /c start "" /min "%~dpnx0" %* /c && exit
set IS_MINIMIZED=

:: kill all python_yf
taskkill /IM python_yf.exe /F
exit