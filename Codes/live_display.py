"""
This file creates a display that shows the values of the slow monitoring live
"""

import numpy as np
import os
import shutil

# Load data
loc1="C:/FTP_root/DATA/acq2106_178/stream.csv"
loc2="C:/FTP_root/DATA/acq2106_377/stream.csv"


def read_n_to_last_line(filename, n = 1):
    """
    Returns the nth before last line of a file (n=1 gives last line)
    I use this because reading the full file can become heavy and slow to load
    https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
    """
    num_newlines = 0
    with open(filename, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return last_line


def txt_2_arr(txt):
    """
    Converts a string to an array
    This is adapted to the output of 1 PeterBox
    None is returned in case of any discrepency
    """
    try :
        lineval=eval(txt)
    except :
        return(None)
    # Sometimes the data reading is partial, in such case, return None
    if len(lineval)==33:
        return(np.array(lineval))
    else:
        return(None)


def seek_last_measurement(location,navg = 5):
    """
    Combining the last two functions (txt_2_array and read_n_to_last_line) to
    properly read the data from the slowmon
    """

    output_data = []

    # navg allows to smooth the reading a bit
    for i in range(navg):
        # i+2 beacause last the line can be partial, and because
        # read_n_to_last_line starts at n=1
        last_line = read_n_to_last_line(location, n = i+2)
        this_line = txt_2_arr(last_line)

        # deal with txt_2_arr error case
        if not this_line is None:
            output_data.append(this_line)
    # if all of the navg reading are errors, return 0
    if output_data == []:
        return(np.zeros(33))
    # else average and output
    output_data=np.array(output_data)
    output_data = np.mean(output_data,axis=0)
    return(output_data)

##

# this is an example of how to fetch data
# data1=seek_last_measurement(loc1)
# data2=seek_last_measurement(loc2)

## Create the nice display with tkinter !
import tkinter as tk
import random

# display speed
update_period = 500 #ms

# background color
backcolor = "#00688B"


def readSensors():
    """
    the function that seeks the data
    """
    data1=seek_last_measurement(loc1,navg=10)
    data2=seek_last_measurement(loc2,navg=10)
    data = np.concatenate((data1[1:],data2[1:]))

    for i in range(len(sensors)):
        # setting up every sensor
        # the variable sensors is defined lower
        value = np.reshape(data,-1)[i]
        if value is None:
            value = 0.0
        sensors[i].set(f"{value:.3f}")  # Truncate to the third decimal place

        # Saturation = red
        if value > 4 or value < -4:
            sensor_labels[i].configure(background='red')
        # Large value = yellow
        elif value >.5 or value <-.5:
            sensor_labels[i].configure(background='yellow')
        # OK = white
        else:
            sensor_labels[i].configure(background='white')

    # wait update_period ticks
    win.after(update_period, readSensors)



# create window
win = tk.Tk()
win.geometry('1550x700')
win.configure(background=backcolor)


# define sensors and labels
sensors = []
sensor_labels = []
num_sensors = 64

# geometry of the displays
num_rows = 4
num_columns = num_sensors // num_rows


# some nice colors to indicate the JPBox cards separation
foreground_colors = ["white","red","yellow","green","orange"]
cards = [
[0,1,2,3,4,5,6,7,8,9,10,11],
[12,13,14,16,17,18,19,20,21,22,23,24],
[25,26,27,28,29,30,32,33,34,35,36,37],
[38,39,40,41,42,43,44,45,46,48,49,50],
[51,52,53,54,55,56,57,58,59,60,61,62]
]
limits = [0,12,25,38,51]

# Create StringVars and Labels
j = 1
k=1
for i in range(num_sensors):
    # if this is the first gage of a JPBox card
    if i in limits:
        channel_label = tk.Label(win, text=f"ch {i+1}\n card {j}",
                             height=2, width=8,
                             font=('Helvetica', 12, 'bold'),
                             background=backcolor,
                             foreground="#e0ac69")
        j+=1

    # if this is a supplementary channel
    elif i%16 == 15:
        channel_label = tk.Label(win,
                             text=f"ch {i+1}\n supp. {k}",
                             height=2, width=8,
                             font=('Helvetica', 12, 'bold'),
                             background=backcolor,
                             foreground="yellow")
        k+=1

    else:
        channel_label = tk.Label(win, text=f"ch {i+1}",
                             height=2, width=8,
                             font=('Helvetica', 12, 'bold'),
                             background=backcolor,
                             foreground="white")

    # create the grid on which to display the labels
    channel_label.grid(row=(i // num_columns) * 2, column=i % num_columns, padx=5, pady=15)


    sensor_var = tk.StringVar()
    sensor_var.set(str(0))  # Initial value
    sensors.append(sensor_var)

    sensor_label = tk.Label(win,
                            textvariable=sensor_var,
                            height=2, width=8,
                            font=('Helvetica', 12, 'bold'),
                            background='white')

    sensor_label.grid(row=i // num_columns * 2 + 1, column=i % num_columns, padx=5, pady=15)
    sensor_labels.append(sensor_label)




win.after(update_period, readSensors)
win.mainloop()
























