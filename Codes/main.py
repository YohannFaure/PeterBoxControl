import tkinter as tk
import os
from tkinter import messagebox
import time

os.chdir("C:/FTP_root/")

# color of background
backcolor = "#00688B"

# Define font style
button_font = ('Arial', 12, 'bold')  # You can adjust the font size and typeface as needed



# Function to create and grid buttons
def create_button(text, file_path, row, column, rowspan=1,confirm = False):
    if confirm:
        button = tk.Button(root, text=text, font=button_font, command=lambda: ask_confirmation(file_path),bg="white")
    else :
        button = tk.Button(root, text=text, font=button_font, command=lambda: launch_batch_file(file_path),bg="white")
    button.grid(row=row, column=column, rowspan=rowspan, pady=10, padx=20, sticky='ew')
    return button  # Return the button widget


# Function to launch the batch file
def launch_batch_file(file_path):
    #os.system(f'start "" /min {file_path} %*')
    os.startfile(file_path)


# Function to ask for confirmation
def ask_confirmation(file_path):
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to clean the data?")
    if confirmed:
        launch_batch_file(file_path)


# Functions to show and hide the additional buttons after the first button is clicked
def show_additional_buttons():
    button_live_display.config(state="normal")
    button_live_plot.config(state="normal")
    button_live_plot_unit.config(state="normal")
    button_demux.config(state="disabled")

def hide_additional_buttons():
    button_live_display.config(state="disabled")
    button_live_plot.config(state="disabled")
    button_live_plot_unit.config(state="disabled")
    button_demux.config(state="normal")


# create a flip-flop switch for the slowmon button
def switched_SM_on():
    """
    Function to launch when clicking a "start Slowmon" button
    """
    button_slowmon.config(
        command=lambda: (
            launch_batch_file("C:/FTP_root/Codes/kill_python_yf.bat"),
            switched_SM_off(),
            hide_additional_buttons()
        ),
        text="\n\nStop slow\nmonitoring\n\n", bg = "red")

def switched_SM_off():
    """
    Function to launch when clicking a "stop Slowmon" button
    """
    button_slowmon.config(
        command=lambda: (
            launch_batch_file("C:/FTP_root/Codes/Slow_Monitoring.bat"),
            show_additional_buttons(),
            switched_SM_on()
        ),
        text="\n\nStart slow\nmonitoring\n\n",
        bg = "white")







# Create the main window
root = tk.Tk()
root.geometry('300x300')
root.configure(background=backcolor)
root.title("Contrôle de la Manip")


# Create the buttons
button_slowmon = create_button("\n\nLaunch slow\nmonitoring\n\n",
                            "C:/FTP_root/Codes/Slow_Monitoring.bat",
                            0, 0,
                            rowspan=3)

button_live_display = create_button("Live Display",
                            "C:/FTP_root/Codes/live_display.bat",
                            0, 1)

button_live_plot = create_button("Live Oscillo",
                            "C:/FTP_root/Codes/live_plot.bat",
                            1, 1)

button_live_plot_unit = create_button("Live Strains",
                            "C:/FTP_root/Codes/live_plot_units.bat",
                            2, 1)

button_demux = create_button("\nDemux\nall files\n",
                            "C:/FTP_root/Codes/Demux_All_Files.bat",
                            3, 0,
                            rowspan=2)

button_clean = create_button("\nClean data\n/!\\\n",
                            "C:/FTP_root/Codes/clean_DATA.bat",
                            3, 1,
                            rowspan=2,
                            confirm = True)

# reconfigure the demux button to disable it for a few second after pressed
# forbids user to launch app multiple times
button_demux.config(
        command=lambda: (
            launch_batch_file("C:/FTP_root/Codes/Demux_All_Files.bat"),
            button_demux.config(state="disabled"),
            time.sleep(2),
            button_demux.config(state="normal")
        )
    )

button_clean.config(bg="yellow")



# initialy hide live_plot
hide_additional_buttons()

# initialy SM is off
switched_SM_off()


# Start the Tkinter event loop
root.mainloop()

