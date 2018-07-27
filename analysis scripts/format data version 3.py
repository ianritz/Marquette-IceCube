import pandas as pd
import os.path
import numpy as np
'''
fstring = input('Are you using Fast Output y/n? ')
if fstring.lower() == 'yes':
    fstring = 'y'
elif fstring.lower() == 'no':
    fstring = 'n'
'''
fstring='n'
#use when analyzing oscilloscope data saved manually from the oscilloscope
def fixOscData():
    data_loc = r'F:\Data\trial 1 3000 Edited\Data' #path to the folder that the data is stored in. MAKE SURE TO CHANGE!!
    if not os.path.exists(data_loc + r' Edited'):
        os.makedirs(data_loc + r' Edited') #makes the folder that the edited data will go into
    
    num_files = len([f for f in os.listdir(path=data_loc)]) #counts the number of files in the data folder
    
    for i in range(0, num_files): #opens up each file in the path given below
        if i < 10: #check to make sure file name has right amount of zeroes
            table = pd.read_csv(data_loc + r'\tek0000'+str(i)+'All.csv', header=None, index_col=None, skiprows=21)
        elif i < 100:
            table = pd.read_csv(data_loc + r'\tek000'+str(i)+'All.csv', header=None, index_col=None, skiprows=21)
        elif i < 1000:
            table = pd.read_csv(data_loc + r'\tek00'+str(i)+'All.csv', header=None, index_col=None, skiprows=21)
        elif i < 10000:
            table = pd.read_csv(data_loc + r'\tek0'+str(i)+'All.csv', header=None, index_col=None, skiprows=21)
        
        if fstring == 'y':
            ntable = table.as_matrix(columns=[0,1,2])
        else:
            ntable = table.as_matrix(columns=[0,1])
        
        #Sets any strings in the data sets to float variables and changes negative infinity values to -.01
        for r in range(0, len(ntable)):
            for h in range(0, 1):
                if isinstance(ntable[r,h], str) and ntable[r,h] != ' -inf' or ntable[r,h] != ' inf':
                    ntable[r,h]=float(ntable[r,h])
                if ntable[r, h] == " -inf":
                    ntable[r,h] = ntable[r-1,h]
                if ntable[r, h] == " inf":
                    ntable[r,h] = ntable[r-1,h]
    
        for r in range(0, len(ntable)):
            ntable[r,1] = -ntable[r,1]
            if fstring == 'y':
                ntable[r,2] = -ntable[r,2]
            
        #Makes new files with the same name as the old ones in a different folder with the corrected values
        df = pd.DataFrame(ntable)
        if i < 10:
            df.to_csv(data_loc + r'\tek0000'+str(i)+'All.csv', index=False)
        elif i < 100:
            df.to_csv(data_loc + r'\tek000'+str(i)+'All.csv', index=False)
        elif i < 1000:
            df.to_csv(data_loc + r'\tek00'+str(i)+'All.csv', index=False)
        elif i < 10000:
            df.to_csv(data_loc + r'\tek0'+str(i)+'All.csv', index=False)
           
#use when analyzing oscilloscope data saved automatically with the computer 
def sepOscTextData():

    trigger_mV = '75'
    dataLoc = r'H:\Flasher' #calls data location
    newLoc = dataLoc + ' ' + str(trigger_mV) + ' Edited' #new file where edited data will be
    outfile = open(newLoc + r'\Output.txt', 'w')
    if not os.path.exists(newLoc):
        os.makedirs(newLoc) #makes the folder that the edited data will go into
    if not os.path.exists(newLoc + r'\Data0'):
        os.makedirs(newLoc + r'\Data0') #makes the folder that the edited data will go into for ch 0
    if not os.path.exists(newLoc + r'\Data1'):
        os.makedirs(newLoc + r'\Data1') #makes the folder that the edited data will go into for ch 1
    if not os.path.exists(newLoc + r'\Data2'):
        os.makedirs(newLoc + r'\Data2') #makes the folder that the edited data will go into for ch 2
    if not os.path.exists(newLoc + r'\Data3'):
        os.makedirs(newLoc + r'\Data3') #makes the folder that the edited data will go into for ch 3
        
    data = pd.read_csv(dataLoc + r'\Dark Noise.txt', header=None, index_col=None, sep=',') #make sure to change file name for correct data
#    if fstring == 'y':    
#        ch1 = data.as_matrix(columns=[0,1,2])
#    if fstring == 'n':
#       ch1 = data.as_matrix(columns=[0,1]

############### Make sure you include the right channels! ###############

    ch1 = data.as_matrix(columns=[0 ,1, 2, 3, 4, 5, 6, 7])
    
    numEvents = int(len(ch1)/10000)
    tList = []
    sList = []
    fList = []

    for i in range(0, numEvents):
        tList = ch1[(10000*i):(10000*i + 10000),0]
        sList0 = ch1[(10000*i):(10000*i + 10000),1]
#        sList1 = (ch1[(10000*i):(10000*i + 10000),3])
#        sList2 = ch1[(10000*i):(10000*i + 10000),5]
#        sList3 = ch1[(10000*i):(10000*i + 10000),7]
        outfile.write(i)
        if fstring == 'y':
            fList = ch1[(10000*i):(10000*i + 10000),2]
            fData = np.column_stack((tList, sList, fList))
        else:
            fData0 = np.column_stack((tList, sList0))
#            fData1 = np.column_stack((tList, sList1))
#            fData2 = np.column_stack((tList, sList2))
#            fData3 = np.column_stack((tList, sList3))
            
        df0 = pd.DataFrame(fData0)
#        df1 = pd.DataFrame(fData1)
#        df2 = pd.DataFrame(fData2)
#        df3 = pd.DataFrame(fData3)
        outfile.write(i + ' again')    
        if i < 10:
            df0.to_csv(newLoc + r'\Data0\tek000'+str(i)+'All.csv', index=False)
#            df1.to_csv(newLoc + r'\Data1\tek000'+str(i)+'All.csv', index=False)
#            df2.to_csv(newLoc + r'\Data2\tek000'+str(i)+'All.csv', index=False)
#            df3.to_csv(newLoc + r'\Data3\tek000'+str(i)+'All.csv', index=False)
        elif i < 100:
            df0.to_csv(newLoc + r'\Data0\tek00'+str(i)+'All.csv', index=False)
#            df1.to_csv(newLoc + r'\Data1\tek00'+str(i)+'All.csv', index=False)
#            df2.to_csv(newLoc + r'\Data2\tek00'+str(i)+'All.csv', index=False)
#            df3.to_csv(newLoc + r'\Data3\tek00'+str(i)+'All.csv', index=False)
        elif i < 1000:
            df0.to_csv(newLoc + r'\Data0\tek0'+str(i)+'All.csv', index=False)
#            df1.to_csv(newLoc + r'\Data1\tek0'+str(i)+'All.csv', index=False)
#            df2.to_csv(newLoc + r'\Data2\tek0'+str(i)+'All.csv', index=False)
#            df3.to_csv(newLoc + r'\Data3\tek0'+str(i)+'All.csv', index=False)
        elif i < 10000:
            df0.to_csv(newLoc + r'\Data0\tek'+str(i)+'All.csv', index=False)
#            df1.to_csv(newLoc + r'\Data1\tek'+str(i)+'All.csv', index=False)
#            df2.to_csv(newLoc + r'\Data2\tek'+str(i)+'All.csv', index=False)
#            df3.to_csv(newLoc + r'\Data3\tek'+str(i)+'All.csv', index=False)
        
 
def fixDataFormat():
    dataLoc = r'C:\Users\Karen\Documents\SignalExpress Data\06072018_100135_AM' #make sure to change to call correct data
    in_file = open(dataLoc + r'\trial3.txt') #make sure to change to call correct data
    out_file = open(dataLoc + r'\trial3_corrected.txt','w') #make sure to change to call correct data
    for line in in_file:
        #replace tabs with commas
        out_file.write(line.replace('\t',','))
        
def fourChannel():
    eventLength = 10000
    trigger_mV = '75'
    dataLoc = r'H:\Flasher' #make sure to change to call correct data
    newLoc = dataLoc + ' ' + str(trigger_mV) + ' Edited'
#    outfile = open(newLoc + r'\Output.txt', 'w')
    if not os.path.exists(newLoc):
        os.makedirs(newLoc) #makes the folder that the edited data will go into
    if not os.path.exists(newLoc + r'\Data0'): #data from channel 0
        os.makedirs(newLoc + r'\Data0')
    if not os.path.exists(newLoc + r'\Data1'): #data from channel 1
        os.makedirs(newLoc + r'\Data1')
    if not os.path.exists(newLoc + r'\Data2'): #data from channel 2
        os.makedirs(newLoc + r'\Data2')
    if not os.path.exists(newLoc + r'\Data3'): #data from channel 3
        os.makedirs(newLoc + r'\Data3')
    i = 0
    for event in pd.read_csv(dataLoc + r'\Dark Noise.txt', header=None, index_col=None, sep=',', chunksize=eventLength):
        data = event.as_matrix(columns=[0, 1, 2, 3, 4, 5, 6, 7])
        time = data[0:, 0]
        ch0 = data[0:, 1] #creates preliminary data columns/lists by channel
        ch1 = data[0:, 3]
        ch2 = data[0:, 5]
        ch3 = data[0:, 7]
        stack0 = np.column_stack((time, ch0)) #creates preliminary data columns/lists by channel
        stack1 = np.column_stack((time, ch1))
        stack2 = np.column_stack((time, ch2))
        stack3 = np.column_stack((time, ch3))
        df0 = pd.DataFrame(stack0) #creates preliminary data columns/lists by channel
        df1 = pd.DataFrame(stack1)
        df2 = pd.DataFrame(stack2)
        df3 = pd.DataFrame(stack3)
        if i < 10:
            df0.to_csv(newLoc + r'\Data0\tek00000'+str(i)+'All.csv', index=False) #name of formatted data file
            df1.to_csv(newLoc + r'\Data1\tek00000'+str(i)+'All.csv', index=False)
            df2.to_csv(newLoc + r'\Data2\tek00000'+str(i)+'All.csv', index=False)
            df3.to_csv(newLoc + r'\Data3\tek00000'+str(i)+'All.csv', index=False)
        elif i < 100:
            df0.to_csv(newLoc + r'\Data0\tek0000'+str(i)+'All.csv', index=False) #name of formatted data file
            df1.to_csv(newLoc + r'\Data1\tek0000'+str(i)+'All.csv', index=False)
            df2.to_csv(newLoc + r'\Data2\tek0000'+str(i)+'All.csv', index=False)
            df3.to_csv(newLoc + r'\Data3\tek0000'+str(i)+'All.csv', index=False)
        elif i < 1000:
            df0.to_csv(newLoc + r'\Data0\tek000'+str(i)+'All.csv', index=False) #name of formatted data file
            df1.to_csv(newLoc + r'\Data1\tek000'+str(i)+'All.csv', index=False)
            df2.to_csv(newLoc + r'\Data2\tek000'+str(i)+'All.csv', index=False)
            df3.to_csv(newLoc + r'\Data3\tek000'+str(i)+'All.csv', index=False)
        elif i < 10000:
            df0.to_csv(newLoc + r'\Data0\tek00'+str(i)+'All.csv', index=False) #name of formatted data file
            df1.to_csv(newLoc + r'\Data1\tek00'+str(i)+'All.csv', index=False)
            df2.to_csv(newLoc + r'\Data2\tek00'+str(i)+'All.csv', index=False)
            df3.to_csv(newLoc + r'\Data3\tek00'+str(i)+'All.csv', index=False)
        elif i < 100000:
            df0.to_csv(newLoc + r'\Data0\tek0'+str(i)+'All.csv', index=False) #name of formatted data file
            df1.to_csv(newLoc + r'\Data1\tek0'+str(i)+'All.csv', index=False)
            df2.to_csv(newLoc + r'\Data2\tek0'+str(i)+'All.csv', index=False)
            df3.to_csv(newLoc + r'\Data3\tek0'+str(i)+'All.csv', index=False)
        elif i < 1000000:
            df0.to_csv(newLoc + r'\Data0\tek'+str(i)+'All.csv', index=False) #name of formatted data file
            df1.to_csv(newLoc + r'\Data1\tek'+str(i)+'All.csv', index=False)
            df2.to_csv(newLoc + r'\Data2\tek'+str(i)+'All.csv', index=False)
            df3.to_csv(newLoc + r'\Data3\tek'+str(i)+'All.csv', index=False)
        i = i + 1

#fixDataFormat()  
#sepOscTextData()
#fixOscData()
fourChannel()