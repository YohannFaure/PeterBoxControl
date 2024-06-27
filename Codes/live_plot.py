"""
This file creates a display that shows the values of the slow monitoring live
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

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


def create_live_data():
    """
    recombine the data from PeterBox 1 and 2
    """
    data1=seek_last_measurement(loc1)
    data2=seek_last_measurement(loc2)
    data = np.concatenate((data1[1:],data2[1:]))
    return(data)

## create plot

import matplotlib.ticker as ticker

# Number of data points to display in each subplot
num_points = 100
period = 500 #ms

# Initialize the figure and axes
fig, axes = plt.subplots(4, 16, sharex=True,sharey=True)
lines = []

x = np.arange(num_points) * period / 1000

# Function to update the plots
def update(frame):
    # Generate new data
    data = create_live_data()
    # Update each subplot with the new data
    for i, ax in enumerate(axes.flat):
        y_data = lines[i].get_ydata()
        y_data = np.roll(y_data, -1)  # Shift data to the left
        y_data[-1] = data[i]  # Insert new data at the end
        lines[i].set_ydata(y_data)
    return lines

# Initialize the subplots and set labels
for i, ax in enumerate(axes.flat):
    ax.set_ylim(-3.5, 3.5)  # Set y-axis limits based on the expected range of PeterBox
    # set up axes
    if i%16!= 0:
        plt.setp(ax.get_yticklabels(), visible=False)
    if i!= 48:
        plt.setp(ax.get_xticklabels(), visible=False)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(period/num_points*4))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(period/num_points*2))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(.5))

    # increase the thickness of the edges
    list_of_spines = ["left", "right", "top", "bottom"]
    C, W, L, T = "black", 1, 1, 1 # <- adjust here
    #Color, Width, Length, Tickness
    for sp in list_of_spines:
        ax.spines[sp].set_linewidth(T)
        ax.spines[sp].set_color(C)


    ax.grid(which = "major")

    ax.text(0.01, 0.99, f"ch. {i+1}", fontsize=8, ha='left', va='top', transform=ax.transAxes)

    line, = ax.plot(x,np.zeros(num_points),c="red")
    lines.append(line)

# adjust spacings
fig.subplots_adjust(left=0.05,
                    bottom=0.05,
                    right=0.95,
                    top=0.95,
                    wspace=0,
                    hspace=0)


# Create an animation that calls the update function every `period` milliseconds)
ani = FuncAnimation(fig, update, interval=period, blit=True,cache_frame_data=False)

# Display the plot
plt.show()

