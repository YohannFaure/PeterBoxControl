"""
This file creates a display that shows the values of the slow monitoring live
The data is shown with units, as configured using the JPBox.
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
    return(add_unit(data))




def V_to_strain(data,amp=2000,G=1.79,i_0=0.0017,R=350):
    """
    Applies the conversion from Voltage to Strain
    amp is the amplification factor
    G is the gauge factor
    i_0 is the fixed current
    R is the gauge resistance
    """
    return(data/(amp*R*G*i_0))

def voltage_to_strains(ch1,ch2,ch3,amp=2000):
    """
    Converts three strain gages channels from bare voltage to real strain
    CH_2 (eps_yy) IS INVERTED TO ENSURE THAT LOADING IS ASSOCIATED WITH INCREASINF EPS.
    """
    # apply different G coefficient to the sides and the center, according
    # to the gages documentation.
    side=lambda x: V_to_strain(x,amp=amp,G=1.79,i_0=0.0017,R=350)
    center=lambda x: -V_to_strain(x,amp=amp,G=1.86,i_0=0.0017,R=350)
    ch1=side(ch1)
    ch2=center(ch2)
    ch3=side(ch3)
    return(ch1,ch2,ch3)


def voltage_to_force(ch):
    """
    Converts Doerler force sensor from voltage to force in kg
    """
    # correct sign
    try :
        for i in range(len(ch)):
            ch[i]=ch[i]*np.median(np.sign(ch[i]))
    except :
        ch = ch*np.median(np.sign(ch))
    return(500/3*ch)

def add_unit(data):
    i=0
    while i<64:
        if i%16 == 15:
            if i<32 :
                data[i] = voltage_to_force(data[i])
            else:
                data[i]*=10
            i+=1
        else:
            data[i],data[i+1],data[i+2] = voltage_to_strains(data[i],data[i+1],data[i+2])
            data[i],data[i+1],data[i+2] = 1000*data[i],1000*data[i+1],1000*data[i+2]
            i+=3
    return(data)


def reposition(data):
    pos = np.array([0,3,6,9,12,16,19,22,25,28,32,35,38,41,44,48,51,54,57,60])

    eps_1 = data[pos]
    eps_2 = data[pos+1]
    eps_3 = data[pos+2]
    forces = data[[15,31,47,63]]
    return(np.concatenate([eps_1,eps_2,eps_3,forces]))


## create plot

import matplotlib.ticker as ticker

# Number of data points to display in each subplot
num_points = 100
period = 500 #ms

# Initialize the figure and axes
fig, axes = plt.subplots(1, 4, sharex=True,sharey="col")
lines = []

x = np.arange(num_points) * period / 1000

# Function to update the plots
def update(frame):
    # Generate new data
    data = create_live_data()
    data = reposition(data)

    # Update each subplot with the new data
    for i in range(len(lines)):
        y_data = lines[i].get_ydata()
        y_data = np.roll(y_data, -1)  # Shift data to the left
        y_data[-1] = data[i]  # Insert new data at the end
        lines[i].set_ydata(y_data)
    return lines

cmap = plt.get_cmap('magma')
colors = [cmap(i/20) for i in range(20)]



# Initialize the subplots and set labels
for i in range(20):
    line, = axes[0].plot(x,np.zeros(num_points),c=colors[i])
    lines.append(line)

for i in range(20):
    line, = axes[1].plot(x,np.zeros(num_points),c=colors[i])
    lines.append(line)

for i in range(20):
    line, = axes[2].plot(x,np.zeros(num_points),c=colors[i])
    lines.append(line)

for i in range(2):
    line, = axes[3].plot(x,np.zeros(num_points))
    lines.append(line)

for i in range(2):
    line, = axes[3].plot(x,np.zeros(num_points),alpha=.5,linewidth=0.5)
    lines.append(line)

for i in range(3):
    axes[i].set_ylim([-2,2])
    axes[i].grid(which="major")

for i in range(3):
    ax=axes[i]
    if i!=0:
        plt.setp(ax.get_yticklabels(), visible=False)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(period/num_points*4))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(period/num_points*2))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(.5))
    ax.set_title(r"$\varepsilon_{}$ (mm/m)".format(i+1))



axes[0].set_xlabel("time (s)")


ax=axes[3]
ax.xaxis.set_major_locator(ticker.MultipleLocator(period/num_points*4))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(period/num_points*2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(200))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(100))
ax.set_title("Forces (kg)")
ax.set_ylim([0,500])
ax.grid(which="major")
ax.yaxis.tick_right()




# Create an animation that calls the update function every `period` milliseconds)
ani = FuncAnimation(fig, update, interval=period, blit=True, cache_frame_data=False)

# Display the plot
plt.show()

