:: launches the python apps that are used for demux


@echo off

echo demuxing all files. This might take a while.

:: relaunch app with minimized command prompt
:: we dont want that here
::if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

:: kill all previously launched demux apps
:: python_yf is a copy of python.exe that I use to distinguish
:: the normal python shells and these python shells
taskkill /IM python_yf.exe /F

:: allow multithreading
setlocal enabledelayedexpansion

:: first PeterBox
cd C:\FTP_root\DATA\acq2106_178\

:: deal with all the files, in parrallel by launching multiple python_yf instances
for %%i in (*.dat) do (
    echo Processing file: %%i
    start /b python_yf C:\FTP_root\Codes\host_demux.py --src=C:\FTP_root\DATA\acq2106_178\%%i --egu=1 --save=npy --savelocation=C:\FTP_root\DATA\acq2106_178 --filename=%%i acq2106_178
)

:: second PeterBox
cd C:\FTP_root\DATA\acq2106_377\

for %%i in (*.dat) do (
    echo Processing file: %%i
    start /b python_yf C:\FTP_root\Codes\host_demux.py --src=C:\FTP_root\DATA\acq2106_377\%%i --egu=1 --save=npy --savelocation=C:\FTP_root\DATA\acq2106_377 --filename=%%i acq2106_377
)


echo All child processes started



:WAIT_LOOP
:: check for any instances of the Python process that are still running
:: only continue when all python_yf are closed, ie when all files have been demuxed
set "running=0"
for /f %%a in ('tasklist^|findstr /bi "python_yf.exe"') do (
    set "running=1"
)

:: if any instances of the Python process are still running, wait for a short period before checking again
if %running% == 1 (
    timeout /t 1 /nobreak > nul
    goto WAIT_LOOP
)

echo All child processes finished


:: start the follow up
start /b "" python_yf C:\FTP_root\Codes\slownmon_recombination.py


python_yf C:\FTP_root\Codes\post_demux.py

