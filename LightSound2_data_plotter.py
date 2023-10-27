##############
## Data plotter for LightSound 2.0
## Code developed by Soley Hyman
## last updated: 06 October 2023 
## Python package requirements: matplotlib, numpy
##############

# Import packages
import numpy as np
import matplotlib.dates as mdates
import sys
from datetime import datetime
from matplotlib import pyplot as plt
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, asksaveasfilename 
from itertools import permutations

# Define functions to read logged LightSound 2.0 data (from .log and .csv files)
def LightSoundReaderV2Raw(inputFilename):
    # make lists
    timezone = ''
    timestamp_list = []
    time_list = []
    lux_list = []
    gain_list = []
    integration_list = []

    # read in input file
    inputDataFile = open(inputFilename)
    lines = inputDataFile.readlines()
    inputDataFile.close()

    # loop over lines
    for l in range(len(lines)):
        currentline = lines[l]
        if currentline.startswith("Timezone"):
            linesplit = currentline.split(None)
            timezone = linesplit[1]			
        if currentline.startswith("Time:"):
            linesplit = currentline.split(None)
            timestamp = linesplit[1] + ' ' + linesplit[2]
            timestamp_fmt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            timestamp_list.append(timestamp_fmt)
        elif currentline.startswith("["):
            linesplit = currentline.split(None)
            time = float(linesplit[1])
            time_list.append(time)
        elif currentline.startswith("Visible"):
            linesplit = currentline.split(None)
            lux = float(linesplit[2])
            lux_list.append(lux)
        elif currentline.startswith("Gain"):
            linesplit = currentline.split(None)
            gain = int(linesplit[1].strip('x'))
            gain_list.append(gain)
        elif currentline.startswith("Integration"):
            linesplit = currentline.split(None)
            integration = int(linesplit[1])
            integration_list.append(integration)
        else:
            pass

    # trim lists to have the same length
    endSeries = np.min([len(i) for i in [timestamp_list, time_list, lux_list, gain_list, integration_list]])
    timestamp_list = timestamp_list[:endSeries]
    time_list = time_list[:endSeries]
    lux_list = lux_list[:endSeries]
    gain_list = gain_list[:endSeries]
    integration_list = integration_list[:endSeries]

    return 	timezone, timestamp_list, time_list, lux_list, gain_list, integration_list


def LightSoundReaderV2Data(inputFilename):

    # make lists
    timezone = ''
    timestamp_list = []
    time_list = []
    lux_list = []
    gain_list = []
    integration_list = []

    # read in input file
    inputDataFile = open(inputFilename)
    lines = inputDataFile.readlines()
    inputDataFile.close()

    # grab timezone
    timezone = lines[0].split(None)[1]

    # loop over lines
    for l in range(2,len(lines)):
        currentline = lines[l]
        linesplit = currentline.strip('\n').split(',')
        timestamp = datetime.strptime(linesplit[0], '%Y-%m-%d %H:%M:%S.%f')
        timestamp_list.append(timestamp)
        time = float(linesplit[1])
        time_list.append(time)
        lux = float(linesplit[2])
        lux_list.append(lux)
        gain = int(linesplit[3])
        gain_list.append(gain)
        integration = int(linesplit[4])
        integration_list.append(integration)

    return 	timezone, timestamp_list, time_list, lux_list, gain_list, integration_list

############################
print('\n')
print('LIGHTSOUND 2.0 DATA PLOTTER')
print()
print("Directions:\nPress Enter after you finish typing into each prompt to continue.\nType 'quit' followed by Enter at any time to exit.")
print('-----------')
# Read in and plot data
exit_quit_misspellings = [''.join(p) for p in permutations('quit')] + [''.join(p) for p in permutations('exit')]

filebrowser = input("\nHow do you want to choose your file?\n   0 = file browser window   1 = manual entry\n   Type 'quit' to exit.\nFile selection method: ").lower()
while (filebrowser=='') or (filebrowser not in ['0','1']) or (filebrowser in exit_quit_misspellings):
    if filebrowser =='':
        filebrowser = input("\nPlease type '0' for file browser or '1' for manual entry: ").lower()
    elif filebrowser in exit_quit_misspellings:
        print('\nExiting program.')
        sys.exit()
    elif filebrowser not in ['0','1']:
        filebrowser = input("\nPlease type '0' for file browser or '1' for manual entry: ").lower()
    else:
        pass

if filebrowser == '0':
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(filetypes=[("CSV files", "*.csv"),("LightSound raw log files", "*_raw.log")]) # show an "Open" dialog box and return the path to the selected file
    while filename == '':
        print('Please select a valid file.')
        filebrowserError = input("\nYou did not select a valid file. Please type 'quit' to exit or press Enter to reselect file: ")
        if filebrowserError in exit_quit_misspellings:
            sys.exit()
        else:
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            filename = askopenfilename(filetypes=[("CSV files", "*.csv"),("LightSound raw log files", "*_raw.log")]) # show an "Open" dialog box and return the path to the selected file
else:
    print('-----------')
    filename = input('\nEnter data filename (with extension): ')
    while (filename=='') or (filename.lower() in exit_quit_misspellings):
        if filename =='':
            filename = input("\nEnter data filename (with extension): ").lower()
        elif filename.lower() in exit_quit_misspellings:
            print('\nExiting program.')
            sys.exit()
        else:
            pass

print('-----------')

plot_lines = input('\nChoose what data to plot.\n   0 = lux data only   1 = lux, gain, and integration-time data\nPlot line choice: ')
while (plot_lines=='') or (plot_lines not in ['0','1']) or (plot_lines in exit_quit_misspellings):
    if plot_lines =='':
        plot_lines = input("\nPlease enter '0' for lux data only or '1' for lux/gain/integration data: ").lower()
    elif plot_lines.lower() in exit_quit_misspellings:
        print('\nExiting program.')
        sys.exit()
    elif plot_lines not in ['0','1']:
        plot_lines = input("\nPlease enter '0' for lux data only or '1' for lux/gain/integration data: ").lower()
    else:
        pass

print('-----------')

plotsaving = input("\nChoose whether to save plot.\n   0 = view plot only   1 = view and save plot.\nPlot saving choice: ").lower()
while (plotsaving=='') or (plotsaving not in ['0','1']) or (plotsaving in exit_quit_misspellings):
    if plotsaving =='':
        plotsaving = input("\nPlease type '0' to view plot only or '1' to save plot: ").lower()
    elif plotsaving in exit_quit_misspellings:
        print('\nExiting program.')
        sys.exit()
    elif plotsaving not in ['0','1']:
        plotsaving = input("\nPlease type '0' to view plot only or '1' to save plot: ").lower()
    else:
        pass

if plotsaving == '1':
    print('-----------')
    if filebrowser == '0':
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        savename = asksaveasfilename(defaultextension=".png", filetypes=(("PNG file", "*.png"),("JPEG file", "*.jpg"),("PDF file", "*.pdf"))) # show an "Save as" dialog box and return the path to the selected file
        while savename == '':
            print('Please enter a valid file prefix.')
            filebrowserError2 = input("\nYou did not select a valid file. Please type 'quit' to exit or press Enter to re-enter save name for plot: ")
            if filebrowserError2 in exit_quit_misspellings:
                sys.exit()
            else:
                Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
                savename = asksaveasfilename(defaultextension=".png", filetypes=(("PNG file", "*.png"),("JPEG file", "*.jpg"),("PDF file", "*.pdf"))) # show an "Save as" dialog box and return the path to the selected file
    else:    
        savename = input('\nEnter filename to save the plot to (with extension): ')
        while (savename=='') or (savename.lower() in exit_quit_misspellings):
            if savename =='':
                savename = input("\nPlease enter filename to save the plot to (with extension): ").lower()
            elif savename.lower in exit_quit_misspellings:
                print('\nExiting program.')
                sys.exit()
            else:
                pass

# Read in data
if filename.split('.')[-1] == 'log': 
    v2_timezone, v2_timestamps, v2_times, v2_lux, v2_gains, v2_integrations = LightSoundReaderV2Raw(filename)
elif filename.split('.')[-1] == 'csv': 
    v2_timezone, v2_timestamps, v2_times, v2_lux, v2_gains, v2_integrations = LightSoundReaderV2Data(filename)

# Plot data
fig, ax = plt.subplots()
if plot_lines == '0': 
    ax.plot(v2_timestamps, v2_lux, color='blue', label='Lux')
elif plot_lines == '1':
    ax.plot(v2_timestamps, v2_lux, color='blue', label='Lux')
    ax.plot(v2_timestamps, v2_gains, color='red', label='Gain')
    ax.plot(v2_timestamps, v2_integrations, color='green', label='Integration')

# Format plot ticks
xformatter = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(xformatter)

# Format plot title and labels
ax.set_title(v2_timestamps[0].strftime('Observations on %Y %b %d starting at %H:%M ') + v2_timezone)
ax.set_xlabel('Local time (%s)' % v2_timezone)
ax.set_ylabel('Intensity (Lux)')
if plot_lines != 0: ax.legend(loc='upper right')

# Save image and show plot
if plotsaving == '1':
    plt.savefig(savename, dpi=500, bbox_inches='tight')
    plt.show()
else:
    plt.show()