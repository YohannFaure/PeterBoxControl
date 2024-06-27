:: relaunch app with minimized command prompt
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 &&  cmd /c start "" /min "%~dpnx0" %* /c  && exit
set IS_MINIMIZED=

:: start the python file
start /b python C:\FTP_root\Codes\main.py

exit