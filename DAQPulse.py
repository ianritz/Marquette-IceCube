import pandas as pd
from ast import literal_eval as le
import numpy as np
from matplotlib import pyplot as plt

#Enter the directory that contains the -P file
dataLoc = r'C:\Users\Karen\Downloads'

#Initializes parameters
leftPulses = []
rightPulses = []



#Formats data to be read by pandas
def fixData():
    #Enter file name
    infile = open(dataLoc + r'\2018-08-01_11-00-27_P_0.06_xy')
    outfile = open(dataLoc + r'\2018-08-01_11-00-27_P_0' + '_CORRECTED.txt', 'w')
    
    #Removes parentheses around each line and separates columns by introducing semicolons
    for line in infile:
        newLine = line[1: -2]
        outfile.write(newLine.replace(', [', ';['))
        outfile.write('\n')
    infile.close()
    outfile.close()



#Filters horizontal coincidence triggers out of two-fold ccoincidecne data and creates TOT plot
def vertCoin():
    #Enter corrected data file
    dataFile = r'\2018-08-01_11-00-27_P_0_CORRECTED.txt'
    
    #Reads data file into matrix of strings (even though they are CLEARLY lists)
    pulses = pd.read_csv(dataLoc + dataFile, sep = ';')
    pulsesArray = pulses.as_matrix()
    
    #Converts those strings into iterable lists
    for l in pulsesArray:
        for i in range(1, 5):
            l[i] = le(l[i])
    
    #Identifies vertical coincidence, sums rising and falling edge times (in nanoseconds?) for every pulse in the two cahnnels, and creates a TOT list for the left side of the detector (channels zero and two) as well as the right side (channels one and three)
    for line in pulsesArray:
        if not line[1] == [] and not line[3] == []:
            for i in range(0, len(line[1])):
                leftPulses.append(sum(line[1][i]))
            for j in range(0, len(line[3])):
                leftPulses.append(sum(line[3][i]))
        if not line[2] == [] and not line[4] == []:
            for i in range(0, len(line[2])):
                rightPulses.append(sum(line[2][i]))
            for j in range(0, len(line[4])):
                rightPulses.append(sum(line[4][i]))
                
    #Automates binning for the data sets            
    if max(leftPulses) > max(rightPulses):
        maxVal = max(leftPulses)
    else:
        maxVal = max(rightPulses)
    if min(leftPulses) < min(rightPulses):
        minVal = min(leftPulses)
    else:
        minVal = min(rightPulses)
    bins = np.arange(np.floor(minVal), np.ceil(maxVal), (maxVal - minVal) / 250)
    
    #Creates TOT histogram for the two data sets
    plt.figure()
    plt.hist([leftPulses, rightPulses], bins = bins)
#    plt.yscale('log')
    plt.legend(['Left-Hand Channels', 'Right-Hand Channels'])
    plt.xlabel('Time(ns)')
    plt.ylabel('Number of Events')
    plt.title('Time Over Threshold')



#Calling functions

#fixData()
vertCoin()