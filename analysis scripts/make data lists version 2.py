import numpy as np
import pandas as pd
import os.path

listLoc = r'H:\Flasher 75 Edited' #file where data list will be located
 
for x in range(0, 3):
    dataLoc = listLoc + r'\Data' + str(x) #path to the data sets, remember to change!
    numFiles = len([f for f in os.listdir(path=dataLoc)])-1 #counts the number of files in the data folder
                   
    #fstring = input('Are you using Fast Output y/n? ')
    #if fstring.lower() == 'yes':
    #    fstring = 'y'
    #elif fstring.lower() == 'no':
    fstring = 'n' #got rid of the beginning of this script asking if using fast output and permanently set to 'n'
    
    trigger = -.0015 #sets the threshold as it is set on the DAQ board IN VOLTS
    
    #Height
    sHeightList = np.zeros(numFiles) #list of Standard Output peak heights
    sMax = 0. #the height of a Standard Output peak
    sMin = -1 #the smallest Standard Output peak
    sPeakTime = 0 #location of the very top of the Standard Output peak
    
    #ToT
    totList = [] #list of time over thresholds for each data set
    sStart = 0 #location of the beginning of the Standard Output peak
    sEnd = 0 #location of the end of the Standard Output peak
    
    #Area
    timeStep = 0. #the time step between two consecutive time data values
    columnAreaList = [] #List of total areas under peak from times start to end
    aboveThreshAreaList = [] #List of areas of peak above threshold
    minAreaList = [] #List of total areas of peak from a minimum threshold value
    columnArea = 0. #Total area under peak from times start to end
    areaAboveThresh = 0. #Area of peak above threshold
    minThreshArea = 0. #Total area of peak from a minimum threshold value
    minThresh = 0.02 #minimum threshold value
    minStart = 0 #beginning of minimum threshold area
    minEnd = 0 #end of minimum threshold area
    minCount = 0 #dataset number of the smallest SOut peak
    
    #Fout Stuff
    fCountList = np.zeros(numFiles) #list of number of Fast Output peaks in each Standard Output peak for each data set
    fHeightList = [] #list of height of each Fast Output peak overall, not for each standard output
    fHolderList = [] #placeholder list that keeps track of the Fast Output peak heights in each Standard Output peak, this list is appended to foutInSoutList
    fInSoutList = [] #a list of lists of Fast Output peak heights in each Standard Output peak
    numSoutPhoton = [] #list of number of photons in each Standard Output peak
    photons = 0 #counts number of photons in one Standard Output peak
    fSlope = 0. #slope of the Fast Output peaks, used to tell when the sign of the slope changes which is indicative of a peak
    fCount = 0 #the number of Fast Output peaks in a Standard Output peak
    smallestEvent = 1. #the smallest Fast Output peak in the whole data folder
    posSlope = False #set to false when the slope goes negative so that a peak is only counted once
    newPeak = False #set to true when the slope goes from negative to positive
    
    #SOut Stuff
    peakTimeList = []
    ToTStartList = []
    peakTime = 0.
    startTime = 0.
    fStart = 0
    fEnd = 0
    
    
    
    #######Check that the .csv files have the right name#######
    for i in range(0, numFiles): #opens up each file in the path given below
        if i < 10: #check to make sure file name has right amount of zeroes with more than 10 files
            dataTable = pd.read_csv(dataLoc + r'\tek00000'+str(i)+'ALL.csv', header=None, index_col=None, skiprows=1)
        elif i < 100:
            dataTable = pd.read_csv(dataLoc + r'\tek0000'+str(i)+'ALL.csv', header=None, index_col=None, skiprows=1)
        elif i < 1000:
            dataTable = pd.read_csv(dataLoc + r'\tek000'+str(i)+'ALL.csv', header=None, index_col=None, skiprows=1)
        elif i < 10000:
            dataTable = pd.read_csv(dataLoc + r'\tek00'+str(i)+'ALL.csv', header=None, index_col=None, skiprows=1)
        elif i < 100000:
            dataTable = pd.read_csv(dataLoc + r'\tek0'+str(i)+'ALL.csv', header=None, index_col=None, skiprows=1)
        elif i < 1000000:
            dataTable = pd.read_csv(dataLoc + r'\tek'+str(i)+'ALL.csv', header=None, index_col=None, skiprows=1)
        dataArray = dataTable.as_matrix(columns=[0,1]) #0=time, 1=sout, 2=fout
    
        timeStep = abs(dataArray[1,0] - dataArray[0,0])*10**9 #the iterations of time steps in the data, set to nanoseconds
    
        #Finds the highest sout peak
        for j in range(0, len(dataArray)): #looping through number of rows in data set
            if dataArray[j,1] < sMax and dataArray[j,1] <= trigger and j < 9900: #checks for the heighest voltage above the trigger level. j<9900 ensures peaks at the very edge of the screen don't give unreasonable data
                sMax = dataArray[j,1]
                sPeakTime = j+1
                peakTime = dataArray[j+1,0]
    
        if sMax > sMin:
            sMin = sMax
            minCount = i
        
        #Finds the begginning and ending points of the Standard Output peak
        for m in range(0, len(dataArray)):
            if dataArray[m,1] > trigger and m <= sPeakTime: #finds the last time the voltage was at or lower the trigger level before the heighest voltage
                sStart = m
                startTime = dataArray[m, 0]  
            elif dataArray[m,1] > trigger and m > sPeakTime and sEnd == 0: #need this to only set end to the first instance of trigger
                sEnd = m + 1   
                
            if dataArray[m,1] > minThresh and m <= sPeakTime: #finds the last time the voltage was at or lower the trigger level before the heighest voltage
                minStart = m   
            elif dataArray[m,1] > minThresh and m > sPeakTime and minEnd == 0: #need this to only set end to the first instance of trigger
                minEnd = m + 1         
                
            if dataArray[m,1] >= 0 and m <= sPeakTime: #finds the start of the sOut peak
                fStart = m
                fStartTime = dataArray[m, 0]
            elif dataArray[m,1] >= 0 and m > sPeakTime and fEnd == 0: #need this to only set end to the first instance of trigger
                fEnd = m + 1
        #Column area under the Standard Output peak and the Fast Output peaks
        for k in range(sStart, sEnd):
            columnArea += dataArray[k, 1]*timeStep #calculates the area under peak from start to end
            areaAboveThresh += ((dataArray[k, 1]*timeStep) - (trigger*timeStep)) #area under peak above threshold from start to end
        #Find information on the FOut signals under a SOut peak
        if fstring == 'y':                         
            for k in range(fStart, fEnd):
                fSlope = dataArray[k, 2] - dataArray[k-1, 2] #finds slope along the Fast Output
                
                if fSlope > 0:
                    posSlope = True
                    newPeak = True
                else:
                    posSlope = False
                    
                if posSlope == False and newPeak == True and fSlope != 0 and dataArray[k-1, 2] >=.102:
                    fCount += 1
                    newPeak = False
                    fHeightList.append(dataArray[k-1, 2])
                    if dataArray[k-1, 2] < smallestEvent:
                        smallestEvent = dataArray[k-1, 2]
                    fHolderList.append(dataArray[k-1, 2])
    
        #Minimum threshold area
        #Finds the begginning and ending points for min threshold
        for k in range(minStart, minEnd):
            minThreshArea += ((dataArray[k, 1]*timeStep) - (minThresh*timeStep)) #calculates the area under peak above a minimum threshold
                
        #Adds the found values to their respective lists
        totList.append(abs(dataArray[sEnd,0] - dataArray[sStart,0])*10**9)
        sHeightList[i] = sMax
        if fstring == 'y':
            fCountList[i] = fCount
            fInSoutList.append(fHolderList)
        peakTimeList.append(peakTime)
        ToTStartList.append(startTime)
        columnAreaList.append(columnArea)
        aboveThreshAreaList.append(areaAboveThresh)
        minAreaList.append(minThreshArea)
    
        #Sets all placeholders to zero
        sPeakTime = 0
        sEnd = 0
        fEnd = 0
        sMax = 0.  
        columnArea = 0.
        areaAboveThresh = 0.
        minThreshArea = 0.
        fCount = 0
        fHolderList = []
            
    #Divides every Fast Output peak by the smallest Fast Output Peak, and adds all the photons to find the total number of photons under a SOut peak
        if fstring == 'y':
            for i in fInSoutList:
                for j in i:
                    photons += j/.102 #.102 was the smallest fast output peak seen
                numSoutPhoton.append(float(format(photons, '.3f'))) #rounds photons to the nearest however many decimal place
                photons = 0
    
    if not os.path.exists(listLoc + r'\Data Lists' + str(x)):
        os.makedirs(listLoc + r'\Data Lists' + str(x)) #makes the folder that the lists will go into
        
    listFolder = (listLoc + r'\Data Lists' + str(x))
    #pd.DataFrame(numSoutPhoton).to_csv(listFolder + r'\Photons in Each Event.csv', index=False)
    
    pd.DataFrame(sHeightList).to_csv(listFolder + r'\Height SOut Peaks.csv', index=False)
    pd.DataFrame(totList).to_csv(listFolder + r'\TOT.csv', index=False)
    pd.DataFrame(peakTimeList).to_csv(listFolder + r'\Peak Time.csv', index=False)
    pd.DataFrame(ToTStartList).to_csv(listFolder + r'\Start Time.csv', index=False)
    if fstring == 'y':
        pd.DataFrame(fCountList).to_csv(listFolder + r'\Number FOut Peaks.csv', index=False)
        pd.DataFrame(fHeightList).to_csv(listFolder + r'\Height FOut Peaks.csv', index=False)
    #for comparing different types of areas of a SOut peak
    pd.DataFrame(columnAreaList).to_csv(listFolder + r'\Column Areas.csv', index=False)
    pd.DataFrame(aboveThreshAreaList).to_csv(listFolder + r'\Areas Above Threshold.csv', index=False)
    #pd.DataFrame(minAreaList).to_csv(listFolder + r'\Min Threshold Areas.csv', index=False)
