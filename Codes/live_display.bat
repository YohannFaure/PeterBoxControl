:: relaunch app with minimized command prompt
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && cmd /c start "" /min "%~dpnx0" %* /c && exit
set IS_MINIMIZED=

python C:/FTP_root/Codes/live_display.py

exit