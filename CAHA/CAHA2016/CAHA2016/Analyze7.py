#V7 removed non-filtered energy col as it is the same as filtered now
#V6 no filtering of spikes, assume consolidate program removed them
#   saves error log file
#   each bin is energy, calculated as 2^bin... was 2^sqrt(bin)
#V5 reads files in directory
#V4 filters out spikes and sorts records
#V3 Ouput: tDays,Energy,Count,Energy/Count,Temp,X,Y,Z,Bin0...BinN
#V2 works with new way of representing time in days (float value) since sensor installed
#V1 reads consolidated file, converts hex to int and expands bins based on max col

import numpy as np
import os
from os import listdir
from os.path import isfile, join

CODE_VERSION=7
energyDir='/Energy/'
MIN_FILE_SIZE=100 # won't process a file unless it is at least this large


def processFile(path,fileName):
    #inFile='C:/Code/Python/Turtle/SamData/TurtleDataAug27/A7.csv'
    #outFile='C:/Code/Python/Turtle/SamData/TurtleDataAug27//A7_Energy.csv'
    inFile=fileName
    a=fileName.split('.')
    outFile=path+energyDir+a[0]+'_Energy.csv'
    THRESH=0.01
    TIME_COL=2 # col of time
    TEMP_COL=4
    X_COL=5
    Y_COL=6
    Z_COL=7
    COUNT_COL=8 # col of count
    BIN_SHIFT_COL=9
    FIRST_BIN_COL=10 # col of first bing
    LAST_BIN_COL=19 # col of first bing
    MAX_BIN_DATA=30 # number of bins possible 
    MAX_BIN_REPORT=10 # number of bins in report
    BIN_DATA_OFFSET=9 # where bins start in data array

    with open(inFile,'r') as ff:
        doc= ff.readlines()

    if len(doc)>MIN_FILE_SIZE:
        print 'creating:',outFile
        fout=open(outFile,'w')

        #load data into array, 0=time 1=energy 2=count 3=energyPerCount 4=energyPerCountFiltered 5=temp 6=X 7=Y 8=Z 9=bin0  etc
        data=np.zeros((len(doc)-1,MAX_BIN_DATA+BIN_DATA_OFFSET))    
        for i in range(1,len(doc)):
            a=doc[i].split(',')
            shift=int(a[BIN_SHIFT_COL], 16)-10
            if (shift<0):
                shift=0;
            data[i-1][0]=float(a[TIME_COL])   # save time stamp
            data[i-1][2]=int(a[COUNT_COL],16)   # save count
            data[i-1][5]=int(a[TEMP_COL],16)   # save temp
            data[i-1][6]=int(a[X_COL],16)   # save X
            data[i-1][7]=int(a[Y_COL],16)   # save Y
            data[i-1][8]=int(a[Z_COL],16)   # save Z

            binCountSum=0    
            for b in range(MAX_BIN_REPORT):
                bbin=b+shift+BIN_DATA_OFFSET
                data[i-1][bbin]=int(a[b+FIRST_BIN_COL],16)   # save bin value, shifted as nececessary
                binCountSum+=int(a[b+FIRST_BIN_COL],16) 
             #compensate for lower bins that are zero if shifted
            if shift>0:
                count=data[i-1][2]
                delta=count-binCountSum
                d=int(delta/shift)
                for j in range(shift):
                    bbin=j+BIN_DATA_OFFSET
                    data[i-1][bbin]=d       # spread extra counts in lower (zero) bins
                    
        # calculate energy
        for i in range(len(doc)-1):
            esum=0
            #sqrt2=2**.5
            for b in range(MAX_BIN_DATA):
                if b==0:    # bin0=no movement so scale=0
                    scale=0
                else:
                    scale=2**(b-1) #  bin1=*2^0 bin2=2^1
                esum+=data[i][b+BIN_DATA_OFFSET]*scale
                #if i==17290:
                 #   print int(b),'\t',data[i][b+BIN_DATA_OFFSET],'\t',int(scale),'\t',int(esum)
            data[i][1]=esum
            
        # calculate energy per count
        for i in range(len(doc)-1):
            energy=data[i][1]
            count=data[i][2]
            epc=1.0*energy/count
            data[i][3]=epc
            
        # sort the array so it's in chronological order
        order = data[:, 0].argsort()
        data = np.take(data, order, 0)

        # filter out spikes... assume filtering is done in consolidea program so just copy data
        data[:,4]=data[:,3] # copy data 
        
        # write header
        fout.write('tDays,Energy,Count,EnergyPerCountFiltered,Temp,X,Y,Z')
        for b in range(0,MAX_BIN_DATA):
            fout.write(',BIN_'+str(b))
        fout.write('\n')

        #save data
        for i in range(len(doc)-1):
            # get values
            time=data[i][0]
            energy=data[i][1]
            count=data[i][2]
            epc=data[i][3]  # energyPerCount
            epcf=data[i][4]  # energyPerCountFiltered
            temp=data[i][5]
            x=data[i][6]
            y=data[i][7]
            z=data[i][8]

            # save values to file
            fout.write(str(time)+','+str(energy)+','+str(count)+','+str(epcf))
            fout.write(','+str(temp)+','+str(x)+','+str(y)+','+str(z))
            for b in range(MAX_BIN_DATA):
                fout.write(','+str(data[i][b+BIN_DATA_OFFSET]))
            fout.write('\n')    
        fout.flush()
        fout.close()
    else:
        print 'ERROR INSUFFICIENT SAMPLES in FILE: ',inFile
        errorLogOut.write('ERRORINSUFFICIENT SAMPLES in FILE: '+inFile+'\n')
    return;

print 'start'
path=os.getcwd()
errorLogOut=open('AnalyzeErrorLog.txt','w') # error log file
errorLogOut.write('Analyze Error Log for all files in directory: '+path+'\n')
errorLogOut.write('Code Version: '+str(CODE_VERSION)+'\n')
files = [ f for f in listdir(path) if isfile(join(path,f)) ]
for f in files:
    a=f.split('.')
    if a[1]=='csv':
        print 'process file:',f
        processFile(path,f)
    else:
        print 'skip file:',f
    print '----------------------------'
errorLogOut.write('Analyze Error Log complete\n')
errorLogOut.flush()
errorLogOut.close()
print 'finished'  

