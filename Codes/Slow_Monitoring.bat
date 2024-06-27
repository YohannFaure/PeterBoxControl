@echo off
:: launches the slow monnitoring

echo Starting Slow Monitoring
echo Close this window at the end of your experiment
echo Closing live display or live plot does not stop the acquisition
echo ~
echo ~
echo ~

setlocal enabledelayedexpansion

:: relaunch app with minimized command prompt
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && cmd /c start /min "" "%~dpnx0" %* /c /min && exit
set IS_MINIMIZED=



:: start the two processes in parrallel for each PeterBox
start /b python_yf C:\FTP_root\Codes\acq400_slowmon.py --egu=1 --show=0 --pchan=32 --save_file=C:\FTP_root\DATA\acq2106_178\stream.csv acq2106_178

start /b python_yf C:\FTP_root\Codes\acq400_slowmon.py --egu=1 --show=0 --pchan=32 --save_file=C:\FTP_root\DATA\acq2106_377\stream.csv acq2106_377


:: close the program and the cmd window when the acquisition
:: is stopped by the control app, using the python_yf trick (see demux)

:WAIT_LOOP
:: check for any instances of the Python process that are still running
set "running=0"
for /f %%a in ('tasklist^|findstr /bi "python_yf.exe"') do (
    set "running=1"
)

:: if any instances of the Python process are still running, wait for a short period before checking again
if %running% == 1 (
    timeout /t 1 /nobreak > nul
    goto WAIT_LOOP
)

echo Closed Slow Monitoring
exit