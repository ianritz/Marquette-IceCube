import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats      

fstring = 'n' #got rid of the beginning of this script asking if using fast output and permanently set to 'n'
trigger_mV = 75 #trigger level in mV, only used in naming of files in Osc Data. change if desired
                
#Osc Data
#sets variables to data files from Make Data Lists.py
oscDataLoc = r'C:\Users\Karen\Documents\SignalExpress Data\Flasher ' + str(trigger_mV) + ' Edited\Data Lists'
#if fstring == 'y':
#    heightFOut = np.asarray(pd.read_csv(oscDataLoc + r'\Height FOut Peaks.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0]
#    numberFOut = np.asarray(pd.read_csv(oscDataLoc + r'\Number FOut Peaks.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0] #Fout in Sout
#    numberPhotons = np.asarray(pd.read_csv(oscDataLoc + r'\Photons in Each Event.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0] # sum of (Fout / lowest Fout)
heightSOut = np.asarray(pd.read_csv(oscDataLoc + r'\Height SOut Peaks.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0]
peakTime = np.asarray(pd.read_csv(oscDataLoc + r'\Peak Time.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0]
startTime = np.asarray(pd.read_csv(oscDataLoc + r'\Start Time.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0]
TOT = np.asarray(pd.read_csv(oscDataLoc + r'\TOT.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0]
oArea = np.asarray(pd.read_csv(oscDataLoc + r'\Areas Above Threshold.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0]
cArea = np.asarray(pd.read_csv(oscDataLoc + r'\Column Areas.csv', header=None, index_col=None, skiprows = 1).as_matrix(columns=[0]))[:,0]

##############################################    Plot functions    #############################################

#plots height of Sout peaks for each data set number
def photonsVsTOT():
    plt.scatter(numberPhotons, TOT, label = 'Lights On', color = 'gold', alpha=0.8) #builds scatter plot (y axis, x axis, title, plot color, plot transparency)
    #plt.scatter(B_NumberPhotons, B_TOT, label = 'Lights Off', color='silver', alpha=.8)
    plt.ylabel('Time Over Threshold (ns)') #labels y axis
    plt.xlabel('Number of Photons') #labels x axis
    plt.title('Probability of Event per Time Over Threshold (Threshold of 3000mV)') #Number of Photons vs Time Over Threshold
    plt.legend(fontsize=11)
    plt.xlim(xmin=0, xmax=25) #dimensions for plot area (change if needed)
    plt.ylim(ymin=0, ymax=40) #dimensions for plot area (change if needed)
    return

    
#histogram of time over threshold values
def histTOT():
    
    bn=np.arange(0, 150, 5) #aranges data in ascending order (start,stop,step size)
    
    plt.figure()
    plt.hist(TOT, bins=bn, alpha = .7, color = 'orange', label = str(len(TOT)) + ' events seen on oscilloscope')
    #plt.yscale('log', nonposy='clip') #sets the y-axis to log-scale
    plt.xticks(range(0, 150, 10))
    plt.xlim([-1, 150]) #dimensions for plot area (change if needed)
    plt.ylim([0, 1000]) #dimensions for plot area (change if needed)
    
    plt.xlabel('Time Over Threhsold (ns)')
    plt.ylabel('log(Number of Events)')
    plt.legend()
    plt.title('Probability of Event per Time Over Threshold (Threshold of 3000mV)')

#plots height of event peak in volts (standard output)
def soutPeakHeights():
    plt.figure()
    plt.plot(heightSOut, label = 'SiPM A', color = 'red', alpha=0.5)
    plt.xlabel('Event Number')
    plt.ylabel('Height of Standard Output Peaks (V)')
    plt.title('Height of Peak per Event') #Number of Photons vs Time Over Threshold
    plt.legend(fontsize=11)
    return

#plots number of fout peaks vs height of Sout peaks
def numFoutVsSoutHeight():
    plt.scatter(heightSOut, numberFOut, label = 'SiPM A', color = 'red', alpha=0.5)
    plt.xlabel('Height of Standard Output Peak (V)')
    plt.ylabel('Number of Fast Output Peaks')
    plt.title('Number of Fout Peaks vs Sout Peak Height') #Number of Photons vs Time Over Threshold
    plt.legend(fontsize=11)
    return

#plots time over threshold for each data set from oscilloscope 
def TOTScope():
    plt.figure()    
    plt.ylabel('Event Number in Data Set')
    plt.xlabel('Time over Threshold (ns)')
    plt.title('Time over Threshold per Event (Threshold 10mV) with Lights Off') #Number of Photons vs Time Over Threshold
    plt.legend(fontsize=11)
    plt.xlim(xmin=0, xmax=200) #dimensions for plot area (change if needed)
    plt.ylim(ymin=0, ymax=2715) #dimensions for plot area (change if needed)
    plt.scatter(TOT, range(0,len(TOT)), color = 'red', alpha=.8)
    #plt.scatter(B_TOT, range(0, len(B_TOT)), color='blue', alpha=0.4)
    return


#plots time over threshold for a given trigger level from oscilloscope data
def TOTbyTriggerScope():
    trigger_level = int(input('Enter trigger level in mV: '))
    if trigger_level >= 30 and trigger_level <= 140:
        trigger_set_number = int((trigger_level/10) - 2)
        start = (10*trigger_set_number - 10)
        end = (start + 10)
        plt.scatter(range(start,end), TOT[start:end], label="SiPM A", color='blue', alpha=0.3)
        #plt.scatter(range(start,end), B_TOT[start:end], label="SiPM B", color='blue')
        plt.xlabel('Event Number in Data Set')
        plt.ylabel('Time over Threshold (ns)')
        plt.legend(fontsize=11)
        plt.suptitle('   Time over Threshold per Event', y=1.0, fontsize=12)
        plt.title('Trigger Level: ' + str(trigger_level) + ' mV', fontsize=10)

    elif trigger_level >= 160 and trigger_level < 700:
        trigger_set_number = int((trigger_level/20)+4)
        start = (trigger_set_number*10)
        end = (start + 10)
        plt.scatter(range(start,end), TOT[start:end], label="SiPM A", color='blue', alpha=0.3)
        #plt.scatter(range(start,end), B_TOT[start:end], label="SiPM B", color='blue')
        plt.xlabel('Event Number in Data Set')
        plt.ylabel('Time over Threshold (ns)')
        plt.legend(fontsize=11)
        plt.suptitle('   Time over Threshold per Event', y=1.0, fontsize=12)
        plt.title('Trigger Level: ' + str(trigger_level) + ' mV', fontsize=10)
        plt.ylim(ymax=25, ymin=-5) #dimensions for plot area (change if needed)
    return
    
    
#plots height of sout and fout peaks for each data set number by trigger level from oscilloscope
def PeakHeightsByTrigger():
    trigger_level = int(input('Enter trigger level in mV: '))
    if trigger_level >= 30 and trigger_level <= 140:
        trigger_set_number = int((trigger_level/10) - 2)
        start = (10*trigger_set_number - 10)
        end = (start + 10)
        plt.plot(range(start,end), heightSOut[start:end], label="Sout A", color='red', alpha=0.3)
        plt.plot(range(start,end), heightFOut[start:end], label="Fout A", color='blue', alpha=0.3)
        plt.xlabel('Event Number')
        plt.ylabel('Height of Standard Output Peak (V)')
        plt.legend(fontsize=10)
        plt.suptitle('   Height of Sout Peak per Event', y=1.0, fontsize=12)
        plt.title('Trigger Level: ' + str(trigger_level) + ' mV', fontsize=10)

    elif trigger_level >= 160 and trigger_level < 700:
        trigger_set_number = int((trigger_level/20)+4)
        start = (trigger_set_number*10)
        end = (start + 10)
        plt.plot(range(start,end), heightSOut[start:end], label="Sout A", color='red', alpha=0.3)
        plt.plot(range(start,end), heightFOut[start:end], label="Fout A", color='blue', alpha=0.3)
        plt.xlabel('Event Number')
        plt.ylabel('Height of Standard Output Peak (V)')
        plt.legend(fontsize=10)
        plt.suptitle('   Height of Sout Peak per Event', y=1.0, fontsize=12)
        plt.title('Trigger Level: ' + str(trigger_level) + ' mV', fontsize=10)
    return


#plots time over threshold vs column area
def cAreaVsTOT():
    plt.figure()
    plt.scatter(TOT, cArea, label="SiPM A", color='green', alpha=0.4)
#    plt.scatter(B_TOT, B_cArea, label="SiPM B", color='blue', alpha=0.3)
    plt.ylabel('Column Area')
    plt.xlabel('Time Over Threshold (ns)')
    plt.title('Column Area vs Time over Threshold')
    plt.legend()
    plt.xlim(xmax=200, xmin=-1) #dimensions for plot area (change if needed)
    plt.ylim(ymax=1, ymin=-12) #dimensions for plot area (change if needed)
    return

#plots time over threshold vs min thresh area
def mAreaVsTOT():
    plt.scatter(TOT, mArea, label="SiPM A", color='green', alpha=0.4)
#    plt.scatter(B_TOT, B_mArea, label="SiPM B", color='blue', alpha=0.3)
    plt.ylabel('Minimum Threshold Area')
    plt.xlabel('Time Over Threshold (ns)')
    plt.title('Min Thresh Area vs Time over Threshold')
    plt.legend()
    plt.xlim(xmax=200, xmin=-1) #dimensions for plot area (change if needed)
    plt.ylim(ymax=1, ymin=-12) #dimensions for plot area (change if needed)
    return

#plots time over threshold vs area above threshold
def oAreaVsTOT():
    plt.figure()
    plt.scatter(TOT, oArea, label="SiPM A", color='green', alpha=0.4)
#    plt.scatter(B_TOT, B_oArea, label="SiPM B", color='blue', alpha=0.3)
    plt.ylabel('Area above Threshold')
    plt.xlabel('Time Over Threshold (ns)')
    plt.title('Area above Threshold vs Time over Threshold')
    plt.legend()
    plt.xlim(xmax=200, xmin=-1) #dimensions for plot area (change if needed)
    plt.ylim(ymax=.1, ymin=-1.5) #dimensions for plot area (change if needed)
    return
    

#plots height of peak vs column area
def HeightVscArea():
    plt.figure()
    plt.scatter(cArea, heightSOut, label="SiPM A", color='orange', alpha=0.4)
#    plt.scatter(B_cArea, B_HeightSOut[0:end], label="SiPM B", color='red', alpha=0.3)
    plt.xlabel('Column Area')
    plt.ylabel('Height of Sout Peak (V)')
    plt.title('Height of Sout Peak vs Column Area')
    plt.legend(fontsize=11)
    plt.xlim(xmax=1, xmin=-12)
    plt.ylim(ymax=.025, ymin=-.1)
    return

#plots height of peak vs min thresh area
def mAreaVsHeight():
    end = len(B_mArea)
    plt.scatter(A_mArea[0:end], A_HeightSOut[0:end], label="SiPM A", color='orange', alpha=0.4)
    plt.scatter(B_mArea, B_HeightSOut[0:end], label="SiPM B", color='red', alpha=0.3)
    plt.xlabel('Minimum Threshold Area')
    plt.ylabel('Height of Sout Peak (V)')
    plt.title('Height of Sout Peak vs Min Thresh Area')
    plt.legend(fontsize=11, loc='upper left')
    plt.xlim(xmax=60, xmin=0) #dimensions for plot area (change if needed)
    plt.ylim(ymax=1, ymin=0) #dimensions for plot area (change if needed)
    return
    
#plots height of peak vs area above threshold
def HeightVsoArea():
    plt.figure()
    plt.scatter(oArea, heightSOut, label="SiPM A", color='orange', alpha=0.4)
    #plt.scatter(B_oArea, B_HeightSOut[0:end], label="SiPM B", color='red', alpha=0.3)
    plt.xlabel('Area above Threshold')
    plt.ylabel('Height of Sout Peak (V)')
    plt.title('Height of Sout Peak vs Area above Threshold')
    plt.legend(fontsize=11)
    plt.xlim(xmax=.1, xmin=-1.5) #dimensions for plot area (change if needed)
    plt.ylim(ymax=.025, ymin=-.04) #dimensions for plot area (change if needed)
    return


#plots number of fout peaks for column area
def cFoutPeaksPerArea():
    plt.scatter(A_cArea, A_NumberFOut, label = 'SiPM A', color = 'orange', alpha=0.7)
    plt.scatter(B_cArea, B_NumberFOut, label = 'SiPM B', color='blue', alpha=0.3)
    plt.ylabel('Number of Fout Peaks')
    plt.xlabel('Column Area')
    plt.title('Number of Fout Peaks per Column Area') #Number of Photons vs Time Over Threshold
    plt.legend(fontsize=11, loc = 'upper left')
    plt.ylim(ymin=0, ymax = 7) #dimensions for plot area (change if needed)
    plt.xlim(xmin=-1, xmax=60) #dimensions for plot area (change if needed)
    return

#plots number of fout peaks for min thresh area
def mFoutPeaksPerArea():
    plt.scatter(A_mArea, A_NumberFOut, label = 'SiPM A', color = 'orange', alpha=0.7)
    plt.scatter(B_mArea, B_NumberFOut, label = 'SiPM B', color='blue', alpha=0.3)
    plt.ylabel('Number of Fout Peaks')
    plt.xlabel('Minimum Threshold Area')
    plt.title('Number of Fout Peaks per Minimum Threshold Area') #Number of Photons vs Time Over Threshold
    plt.legend(fontsize=11, loc = 'upper left')
    plt.ylim(ymin=0, ymax = 7) #dimensions for plot area (change if needed)
    plt.xlim(xmin=-1, xmax=60) #dimensions for plot area (change if needed)
    return

#plots number of fout peaks for area above threshold
def oFoutPeaksPerArea():
    plt.scatter(A_oArea, A_NumberFOut, label = 'SiPM A', color = 'orange', alpha=0.7)
    plt.scatter(B_oArea, B_NumberFOut, label = 'SiPM B', color='blue', alpha=0.3)
    plt.ylabel('Number of Fout Peaks')
    plt.xlabel('Area above Threshold')
    plt.title('Number of Fout Peaks per Area above Threshold') #Number of Photons vs Time Over Threshold
    plt.legend(fontsize=11, loc = 'upper left')
    plt.ylim(ymin=0, ymax = 7) #dimensions for plot area (change if needed)
    plt.xlim(xmin=-1, xmax=15) #dimensions for plot area (change if needed)
    return

#plots number of fout peaks for each time over threshold from oscilloscope data
def FoutPeaksPerTOT():
    plt.scatter(A_TOT, A_NumberFOut, label = 'SiPM A', color = 'red', alpha=0.7)
    plt.scatter(B_TOT, B_NumberFOut, label = 'SiPM B', color='blue', alpha=0.3)
    plt.ylabel('Number of Fout Peaks')
    plt.xlabel('Time over Threshold (ns)')
    plt.title('Number of Fout Peaks per ToT (Threshold 700mV)') #Number of Photons vs Time Over Threshold
    plt.legend(fontsize=11, loc = 'upper left')
    plt.ylim(ymin=0, ymax = 7) #dimensions for plot area (change if needed)
    plt.xlim(xmax=140) #dimensions for plot area (change if needed)
    return
    
#plots time over threshold vs height of peak for oscilloscope data
def HeightVsTOT():
    plt.figure()
    plt.scatter(TOT, heightSOut, label="SiPM A", color='blue', alpha=0.4)
#    plt.scatter(B_TOT, B_HeightSOut, label="SiPM B", color='gray', alpha=0.3)
    plt.ylabel('Height of Sout Peak (V)')
    plt.xlabel('Time Over Threshold (ns)')
    plt.title('Height of Sout Peak vs ToT (Threshold 700mV)')
    plt.legend(fontsize=11)
    plt.xlim(xmax=200, xmin=-1) #dimensions for plot area (change if needed)
    plt.ylim(ymax=.025, ymin=-.1) #dimensions for plot area (change if needed)
    return


#plots time over threshold vs height of peak for oscilloscope data
def HeightByTrigger():
#    plt.scatter(Trigger_L, A_HeightSOut, label="SiPM A", color='purple', alpha=0.4)
#    plt.scatter(Trigger_L, B_HeightSOut, label="SiPM B", color='gray', alpha=0.3)
    plt.ylabel('Height of Peak (V)')
    plt.xlabel('Trigger Level (mV)')
    plt.title('Height of Peak vs Trigger Level')
    plt.legend(fontsize=11, loc='upper left')
    plt.xlim(xmax=750, xmin=0) #dimensions for plot area (change if needed)
    plt.ylim(ymax=1, ymin=0) #dimensions for plot area (change if needed)
    return 
    
    
#plots height vs trigger level for oscilloscope
def TOTbyTrigger():
#    plt.scatter(A_TOT, Trigger_L, label="SiPM A", color='red', alpha=0.4)
#    plt.scatter(B_TOT, Trigger_L, label="SiPM B", color='purple', alpha=0.3)
    plt.ylabel('Trigger Level (mV)')
    plt.xlabel('Time Over Threshold (ns)')
    plt.title('Trigger Level vs ToT')
    plt.legend(fontsize=11)
    plt.xlim(xmax=120, xmin=-1) #dimensions for plot area (change if needed)
    plt.ylim(ymax=750, ymin=0) #dimensions for plot area (change if needed)
    return  


#plots time over threshold for DAQ board data
def TOTDAQ():
#    if len(ToTCh0) == len(ToTCh1):
#        start = 0
#        end = len(ToTCh0)

#    plt.scatter(range(start,end), ToTCh0, label = 'Ch0', color='red', alpha=1)
#    plt.scatter(range(start,end), ToTCh1, label = 'Ch1', color = 'purple', alpha=0.5)
    plt.xlabel('Event Number')
    plt.ylabel('Time over Threshold (ns)')
    plt.suptitle('   Time over Threshold per Event', y=1.0, fontsize=12)
    plt.title('Trigger Level: 170 mV', fontsize=10)
    plt.legend(fontsize=10)
    plt.ylim(ymax=25, ymin=0) #dimensions for plot area (change if needed)
    return


#plots time over threshold for scope and DAQ board together
def TOTScopeVsDAQ():
    trigger_level = int(input('Enter trigger level in mV: '))
    if trigger_level >= 30 and trigger_level <= 140:
        trigger_set_number = int((trigger_level/10) - 2)
        start = (10*trigger_set_number - 10)
        end = (start + 10)
    elif trigger_level >= 160 and trigger_level < 700:
        trigger_set_number = int((trigger_level/20)+4)
        start = (trigger_set_number*10)
        end = (start + 10)
        
    #Ordering data points
    for k in A_TOT[start:end]:
        for m in range(0,9):
            if A_TOT[start:end][m] > A_TOT[start:end][m+1]:
                temp = A_TOT[start:end][m]
                A_TOT[start:end][m] = A_TOT[start:end][m+1]
                A_TOT[start:end][m+1] = temp
        
    for k in B_TOT[start:end]:
        for m in range(0,9):
            if B_TOT[start:end][m] > B_TOT[start:end][m+1]:
                temp = B_TOT[start:end][m]
                B_TOT[start:end][m] = B_TOT[start:end][m+1]
                B_TOT[start:end][m+1] = temp

    print(A_TOT[start:end])
    print(B_TOT[start:end])

    plt.scatter(range(0,10), B_TOT[start:end], color='blue', label = 'Scope', alpha=0.4)
    plt.xlim(xmax=14, xmin=-1) #dimensions for plot area (change if needed)
    plt.ylim(ymax=14, ymin=-1) #dimensions for plot area (change if needed)
    plt.xlabel('DAQ Time over Threshold (ns)')
    plt.ylabel('Scope Time over Threshold (ns)')
    plt.suptitle('   Time over Threshold', y=1.0, fontsize=12)
    plt.title('Trigger Level: 170 mV', fontsize=10)
    plt.legend(fontsize=11, loc='upper left')
    return

    
#plots the gradient colormesh for time over threshold
#def gradient():
    #H, xedges, yedges = np.histogram2d(B_NumberPhotons, B_TOT, bins = 50)
    #H = H.T
    #plt.pcolormesh(xedges, yedges, H, cmap=plt.get_cmap('OrRd'))
    #return


#plot individual event
def PlotEvent():
    start= -.000002
    end= .000002
    TL= 0.7
#    plt.plot(B_398Time, B_398Sout, label = 'Sout', color = 'red', alpha=0.4)
#    plt.plot(B_398Time, B_398Fout, label = 'Fout', color = 'blue', alpha=0.4)
    plt.plot((start, end), (TL, TL), lw=1, color='purple')
    plt.ylabel('V')
    plt.xlabel('Time')
    plt.title('Event 398')
    plt.legend(fontsize=11)
    #plt.ylim(ymin=-.01, ymax=0.08)
    #plt.xlim(xmin=-.000000025, xmax=.0000002)
    return

    
#trying again to plot individual events by searching through columns in file - not working HALP
def PlotEvents():
    time = []
    sout = []
    fout = []
#    for j in range(0, len(dataFileB)):
#        for k in dataFileB:
#            time = int(dataFileB[k][0])
#            sout = int(dataFileB[k][1])
#            fout = int(dataFileB[k][2])
    plt.plot(time, sout, label = 'Sout', color='red', alpha=0.4)
    plt.plot(time, fout, label = 'Fout', color='blue', alpha=0.3)
    plt.ylabel('V')
    plt.xlabel('Time')
    plt.title('Individual Event')
    plt.legend(fontsize=11)

#creates histogram of event heights (standard output)
def histHeight():
    
    bn=np.arange(-.01,0,.00025) #aranges data in ascending order (start,stop,step size)
    
    plt.figure()
    plt.hist(heightSOut, bins=bn, alpha = .7, color = 'orange', label = str(len(heightSOut)) + ' events seen on oscilloscope')
    #plt.yscale('log', nonposy='clip') #sets the y-axis to log-scale
    #plt.xscale('log', nonposy='clip')
    plt.xticks(np.arange(-.01, -.00025, .0025))
    plt.xlim([-.01, -.0025]) #dimensions for plot area (change if needed)
    plt.ylim([0, 250]) #dimensions for plot area (change if needed)
    
    plt.xlabel('Height of Sout Peak (V)')
    plt.ylabel('Number of Events')
    plt.legend()
    plt.title('Peak Spectrum')
    
def histcArea():
    
    bn=np.arange(-1.5, 0, .005) #aranges data in ascending order (start,stop,step size)
    
    plt.figure()
    plt.hist(cArea, bins=bn, alpha = .7, color = 'orange', label = str(len(cArea)) + ' events seen on oscilloscope')
    #plt.yscale('log', nonposy='clip') #sets the y-axis to log-scale
    #plt.xscale('log', nonposy='clip')
    plt.xticks(np.arange(-1.5, 0, .25))
    plt.xlim([-1.5, 0]) #dimensions for plot area (change if needed) 
    plt.ylim([0, 100]) #dimensions for plot area (change if needed)
    
    plt.xlabel('Column Area')
    plt.ylabel('Number of Events')
    plt.legend()
    plt.title('Column Area Histogram')

#creates histogram of relative charge per event    
def histoArea():
    
    bn=np.arange(-1.375, 0, .005) #aranges data in ascending order (start,stop,step size)
    
    plt.figure()
    plt.hist(oArea, bins=bn, alpha = .7, color = 'orange', label = str(len(oArea)) + ' events seen on oscilloscope')
    #plt.yscale('log', nonposy='clip') #sets the y-axis to log-scale
    #plt.xscale('log', nonposy='clip')
    plt.xticks(np.arange(-1.5, 0, .25))
    plt.xlim([-1.375, 0]) #dimensions for plot area (change if needed)
    plt.ylim([0, 100]) #dimensions for plot area (change if needed)
    
    plt.xlabel('Area Over Threshold')
    plt.ylabel('Number of Events')
    plt.legend()
    plt.title('Relative Charge Per Event')
######################################    calling functions    ###########################################

############### Standard Output Plots ###############

#soutPeakHeights()
#TOTScope()
#cAreaVsTOT()
#oAreaVsTOT()
#histTOT()
#HeightVscArea()
#HeightVsoArea()
#HeightVsTOT()
#histHeight()
#histcArea()
#histoArea()

############### Fast Output Plots ###############

#numFoutVsSoutHeight()
#photonsVsTOT()
#cFoutPeaksPerArea()
#mFoutPeaksPerArea()
#oFoutPeaksPerArea()
#FoutPeaksPerTOT()

############## Not Working ###############

#PlotEvents()
#TOTbyTriggerScope()
#PeakHeightsByTrigger()
#mAreaVsTOT()
#mAreaVsHeight()
#HeightByTrigger()
#TOTbyTrigger()
#TOTDAQ()
#TOTScopeVsDAQ()
#gradient()
#PlotEvent()
