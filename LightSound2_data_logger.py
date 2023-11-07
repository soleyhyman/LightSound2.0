##############
## Serial logger for LightSound 2.0
## Code developed by Soley Hyman, with help from G M's code at: https://electronics.stackexchange.com/questions/54/saving-arduino-sensor-data-to-a-text-file */
## last updated: 06 October 2023
## Python package requirements: numpy, matplotlib, pySerial (https://pyserial.readthedocs.io/en/latest/pyserial.html#installation), datetime, sys
##############

# coding=utf-8

# Import packages
import serial
import sys
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import permutations
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import asksaveasfilename 
import os
import time
import serial.tools.list_ports

# Define function to read logged LightSound 2.0 data
def LightSoundReaderV2Log(inputFilename):
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

    # loop over lines
    for l in range(len(lines)):
        currentline = lines[l]
        if currentline.startswith("Timezone"):
            linesplit = currentline.split(None)
            timezone = linesplit[1]			
        if currentline.startswith("Time:"):
            linesplit = currentline.split(None)
            timestamp = linesplit[1] + ' ' + linesplit[2]
            timestamp_list.append(timestamp)
        elif currentline.startswith("["):
            linesplit = currentline.split(None)
            time_list.append(linesplit[1])
        elif currentline.startswith("Visible"):
            linesplit = currentline.split(None)
            lux_list.append(linesplit[2])
        elif currentline.startswith("Gain"):
            linesplit = currentline.split(None)
            gain = linesplit[1].strip('x')
            gain_list.append(gain)
        elif currentline.startswith("Integration"):
            linesplit = currentline.split(None)
            integration_list.append(linesplit[1])
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

# Animation function that also reads in data from 
# serial port and writes to file
def animate(i, times, luxes):
    timeNow = datetime.now()
    line = ser.readline()
    line = line.decode("utf-8")
    if line.startswith('['):
        f.writelines('Time: ' + str(timeNow) + '\n')
        print('Time:', timeNow)
        f.writelines([line])
        print(line.strip('\n'))	
    elif line.startswith('Visible'):
        f.writelines([line])
        print(line.strip('\n'))	
        times.append(timeNow)
        luxes.append(float(line.split(None)[2]))
    else:
        f.writelines([line])
        print(line.strip('\n'))
    
    # plot data
    ax.clear()
    ax.plot(times, luxes)
    ax.set_title(initialTime.strftime('Observations on %Y %b %d starting at %H:%M ') + timezone)
    ax.set_xlabel('Local time (%s)' % timezone)
    ax.set_ylabel('Intensity (Lux)')

##################################
exit_quit_misspellings = [''.join(p) for p in permutations('quit')] + [''.join(p) for p in permutations('exit')]
baud_rate = int(9600)	# Should be 9600 for LightSound 2.0

print('\n')
print('LIGHTSOUND 2.0 DATA LOGGER')
print()

ports = serial.tools.list_ports.comports()
if len(ports) == 0:
    print('\nNo LightSound port detected. Make sure your device is plugged in with a USB cable\ncapable of data transfer. If you have a PCB LightSound, make sure it is switched on.\n\nExiting program.')
    sys.exit()
else:
    pass

print("Directions:\nPress Enter after you finish typing into each prompt to continue.\nType 'quit' followed by Enter at any time to exit.")
print("Once the data logging begins, click into this window and use the Ctrl+C command to end logging.")
print('-----------')

# Read arguments from command line
# language = input("Select language:\n   0 = English   1 = Español   2 = Français.\nEnter language ID or type 'quit' to exit and press enter: ").lower()
# while (language == '') or (language in exit_quit_misspellings) or (language not in ['0','1','2']):
#     if language == '':
#         language = input("Please type '0' for English, '1' for Español, '2' for Français: ").lower()
#     elif language in exit_quit_misspellings:
#         time.sleep(1.5)
#         sys.exit()
#     elif language not in ['0','1','2']:
#         language = input("Please type '0' for English, '1' for Español, '2' for Français: ").lower()

# if language == '0':
#     pass
# elif language == '1':
#     pass
# elif language == '2':
#     pass
# else:
#     pass

# print('-----------')

# Read arguments from command line
print('\nIdentifying serial port for LightSound')
ports = serial.tools.list_ports.comports()
# while len(ports) == 0:
#     print('No LightSound port detected. Make sure your device is plugged in with a USB cable\ncapable of data transfer. If you have a PCB LightSound, make sure it is switched on.')
#     while (portID=='') or (portID in exit_quit_misspellings) or (portID not in numPortRangeIDs):
#         if portID=='':
#             portID = input("\nPlease enter a number between {} and {}: ".format(numPortRange[0],numPortRange[-1]))
#         elif portID.lower() in exit_quit_misspellings:
#             print('\nExiting program.')
#             time.sleep(1.5)
#             sys.exit()            
#         if portID not in numPortRangeIDs:
#             portID = input("\nPlease enter a number between {} and {}: ".format(numPortRange[0],numPortRange[-1]))
#         else:
#             pass
if len(ports) == 1:
    print('Only one port found at ' + str(ports[0]))
    print('Connecting to port.')
    serial_port = ports[0][0]
else:
    numPortRange = range(len(ports))
    numPortRangeIDs = [str(i) for i in numPortRange]
    print("There are more than one available port identified. Please choose from the list below.\n   Windows: the port should start with COM, followed by a number\n   Mac: the port should have the form /dev/tty.usbmodem* or /dev/tty.usbserial*\n   Linux: the port should have the form /dev/ttyUSB* or /dev/ttyACM*")
    print("Available ports:")
    for i in numPortRange: print(str(i) + ' - ' + str(ports[i]))
    portID = input("Please enter the number (i.e., {} - {}) corresponding to the desired port: ".format(numPortRange[0],numPortRange[-1])).lower()
    while (portID=='') or (portID in exit_quit_misspellings) or (portID not in numPortRangeIDs):
        if portID=='':
            portID = input("\nPlease enter a number between {} and {}: ".format(numPortRange[0],numPortRange[-1]))
        elif portID.lower() in exit_quit_misspellings:
            print('\nExiting program.')
            time.sleep(1.5)
            sys.exit()            
        if portID not in numPortRangeIDs:
            portID = input("\nPlease enter a number between {} and {}: ".format(numPortRange[0],numPortRange[-1]))
        else:
            pass
    serial_port = ports[int(portID)][0]

print('-----------')

timezone = input("\nSpecify the timezone of your observations (e.g., CST, EST, ART, CLT, etc.): ")
while (timezone=='') or (timezone.lower() in exit_quit_misspellings):
    if timezone =='':
        timezone = input("\nPlease enter the timezone: ")
    elif timezone.lower() in exit_quit_misspellings:
        print('\nExiting program.')
        time.sleep(1.5)
        sys.exit()        
    else:
        pass

print('-----------')

filebrowser = input("\nHow do you want to choose the filename and location of your?\n   0 = file browser window   1 = manual entry\nFile selection method: ").lower()
while (filebrowser=='') or (filebrowser not in ['0','1']) or (filebrowser in exit_quit_misspellings):
    if filebrowser =='':
        filebrowser = input("\nPlease type '0' for file browser or '1' for manual entry: ").lower()
    elif filebrowser in exit_quit_misspellings:
        print('\nExiting program.')
        time.sleep(1.5)
        sys.exit()        
    elif filebrowser not in ['0','1']:
        filebrowser = input("\nPlease type '0' for file browser or '1' for manual entry: ").lower()
    else:
        pass
if filebrowser == '0':
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    file_prefix = asksaveasfilename(defaultextension="", filetypes=(("File prefix", ""),)).strip('_raw.log').strip('_data.csv')
    while file_prefix == '' or os.path.isfile(file_prefix+'_raw.log') or os.path.isfile(file_prefix+'_data.csv'):
        if file_prefix == '':
            print('Please enter a valid file prefix.')
            filebrowserError = input("\nYou did not enter a valid file prefix. Please type 'quit' to exit or press Enter to re-enter file prefix: ")
            if filebrowserError in exit_quit_misspellings:
                time.sleep(1.5)
                sys.exit()                
            else:
                Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
                file_prefix = asksaveasfilename(defaultextension="", filetypes=(("File prefix", ""),)).strip('_raw.log').strip('_data.csv')
        elif os.path.isfile(file_prefix+'_raw.log') or os.path.isfile(file_prefix+'_data.csv'):
            overwriteYN = input("\nA file with that prefix already exists. Do you want to overwrite? (type 'y' for yes or 'n' for no)\ny or n: ").lower()
            if overwriteYN in exit_quit_misspellings:
                time.sleep(1.5)
                sys.exit()                
            elif overwriteYN not in ['y','n']:
                overwriteYN = input("\nPlease type 'y' to overwrite exisiting files or 'n' to choose a different name.\ny or n: ").lower()
            elif overwriteYN == 'y':
                break
            else:
                Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
                file_prefix = asksaveasfilename(defaultextension="", filetypes=(("File prefix", ""),)).strip('_raw.log').strip('_data.csv')
else:
    file_prefix = input("\nSpecify the filename prefix for the data files. Do not include an extension.\nFilename prefix: ")
    while (file_prefix=='') or (file_prefix.lower() in exit_quit_misspellings) or os.path.isfile(file_prefix+'_raw.log') or os.path.isfile(file_prefix+'_data.csv'):
        if file_prefix =='':
            file_prefix = input("\nPlease enter the filename prefix: ")
        elif file_prefix.lower() in exit_quit_misspellings:
            print('\nExiting program.')
            time.sleep(1.5)
            sys.exit()            
        elif os.path.isfile(file_prefix+'_raw.log') or os.path.isfile(file_prefix+'_data.csv'):
            overwriteYN = input("\nA file with that prefix already exists. Do you want to overwrite? (type 'y' for yes or 'n' for no)\ny or n: ").lower()
            if overwriteYN in exit_quit_misspellings:
                time.sleep(1.5)
                sys.exit()                
            elif overwriteYN not in ['y','n']:
                overwriteYN = input("\nPlease type 'y' to overwrite exisiting files or 'n' to choose a different name.\ny or n: ").lower()
            elif overwriteYN == 'y':
                break
            else:
                file_prefix = input("\nPlease enter a new filename prefix: ")

print('-----------')

# liveplotting = input("\nDo you want to show the live-plotting graph? Type 'y' if yes and 'n' if no.\ny or n: ").lower()
# while (liveplotting=='') or (liveplotting in exit_quit_misspellings) or (liveplotting not in ['y','n']):
#     if liveplotting =='':
#         liveplotting = input("\nType 'y' for liveplot and 'n' for no liveplot: ").lower()
#     elif (liveplotting=='quit') or (liveplotting=='exit'):
#         print('\nExiting program.')
#         time.sleep(1.5)
#         sys.exit()        
#     elif liveplotting not in ['y','n']:
#         liveplotting = input("\nType 'y' for liveplot and 'n' for no liveplot: ").lower()
#     else:
#         pass

liveplotting = 'n'

print('\n-----------')

# Create serial port
ser = serial.Serial(serial_port, baud_rate)

if liveplotting ==  'y':
    # Create figure and axis for liveplotting
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    times = []
    luxes = []
    plottingLine, = ax.plot(times,luxes, color='b', zorder=1)

    # Format plot title and labels
    initialTime = datetime.now()
    ax.set_title(initialTime.strftime('Observations on %Y %b %d starting at %H:%M ') + timezone)
    ax.set_xlabel('Local time (%s)' % timezone)
    ax.set_ylabel('Intensity (Lux)')

    # Open logging file and begin logging data
    with open(file_prefix + '_raw.log', 'w+') as f:
        print('Timezone:', timezone, '\n')
        f.writelines('Timezone: ' + timezone + '\r \n')
        while True:
            try:
                ani = animation.FuncAnimation(fig, animate, fargs=(times, luxes), interval=50)
                plt.show()
            except KeyboardInterrupt:
                plt.savefig(file_prefix + "_livePlot.png", dpi=300)
                f.close()
                print('Logging terminated')
                break
else:
    # Open logging file and begin logging data
    with open(file_prefix + '_raw.log', 'w+') as f:
        print('Timezone:', timezone, '\n')
        f.writelines('Timezone: ' + timezone + '\r \n')
        while True:
            try:
                timeNow = datetime.now()
                line = ser.readline()
                line = line.decode("utf-8")
                if line.startswith('['):
                    f.writelines('Time: ' + str(timeNow) + '\n')
                    print('Time:', timeNow)
                    f.writelines([line])
                    print(line.strip('\n'))	
                elif line.startswith('Visible'):
                    f.writelines([line])
                    print(line.strip('\n'))	
                    # times.append(timeNow)
                    # luxes.append(float(line.split(None)[2]))
                else:
                    f.writelines([line])
                    print(line.strip('\n'))
            except KeyboardInterrupt:
                # plt.savefig(file_prefix + "_livePlot.png", dpi=300)
                f.close()
                print('Logging terminated')
                break

############################

# Read logged data and save it as columns in tab separated file

# Read in logged data
v2_timezone, v2_timestamps, v2_times, v2_lux, v2_gains, v2_integrations = LightSoundReaderV2Log(file_prefix+'_raw.log')

# Group data by rows
with open(file_prefix+'_data.csv', 'w+') as col_file:
    col_file.writelines('Timezone: ' + timezone + '\n')
    col_file.writelines('Timestamp, Time (ms), Lux, Gain, Integration\n')

    for i in range(len(v2_timestamps)):
        data_row = [v2_timestamps[i], v2_times[i], v2_lux[i], v2_gains[i], v2_integrations[i]]
        col_file.writelines(','.join(data_row) + '\n')

print('Logged data saved in columns')
col_file.close()