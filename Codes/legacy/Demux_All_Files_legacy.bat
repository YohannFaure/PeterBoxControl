start /b "" python C:\FTP_root\Codes\slownmon_recombination.py

cd C:\FTP_root\DATA\acq2106_178\


for %%i in (*.dat) do (python C:\FTP_root\Codes\host_demux.py --src=C:\FTP_root\DATA\acq2106_178\%%i --egu=1 --save=npy --savelocation=C:\FTP_root\DATA\acq2106_178 --filename=%%i acq2106_178)


cd C:\FTP_root\DATA\acq2106_377\

for %%i in (*.dat) do (python C:\FTP_root\Codes\host_demux.py --src=C:\FTP_root\DATA\acq2106_377\%%i --egu=1 --save=npy --savelocation=C:\FTP_root\DATA\acq2106_377 --filename=%%i acq2106_377)


python C:\FTP_root\Codes\post_demux.py

