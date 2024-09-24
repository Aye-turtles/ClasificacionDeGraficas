# V7
# remove first few samples of record to remove glitch from radio power on
# error log is saved as file

# V6
# processes all directories

# V5
# now report time in days (float) from sensor install date

# V4
# reads raw files downloaded from server and consolidates into one file
# adds file, sensor, and absolute time stamp
# warning: output file is not necessarily in chrononlogical (time stamp) order

import os
from os import listdir
from os.path import isfile, join
from calendar import monthrange

CODE_VERSION=7
DATA_COL=17 # number of columns in a valid row of data
HEADER_COL=8 # number of columns in a valid header
SEC_PER_REC_COL=1 # column with seconds per record
SKIP_COUNT=3 # skips first SKIP_COUNT records to remove power-on caused spike in report
def getInstallTime(b):  # format of b='2014-06-20'
    dd=b.split('-')
    year=int(dd[0])
    month=int(dd[1])
    sumDay=int(dd[2])
    for m in range(1,month):
        mr=monthrange(year,m)  # returns weekday of first day of the month and number of days in month
        sumDay+=mr[1] # days in month
    return(sumDay*3600*24)

def getSensorReport(f):
    try:
        a=f.split('_')
        sensor=a[1]
        b=a[2].split('-')
        c=b[2].split('.')
        report=int(b[1])*100+int(c[0])
        return(sensor,report)
    except:
        print 'FILE NAME FORMAT ERROR:',f
        errorLogOut.write('FILE NAME FORMAT ERROR: '+f+'\n')
        return(0,0)

def getAbsTime(dt):   # ['Report date/time: 2014/08/02', '07:41:17']
    #get date
    d=dt[0].split()
    dd=d[2].split('/')
    year=int(dd[0])
    month=int(dd[1])
    sumDay=int(dd[2])
    for m in range(1,month):
        mr=monthrange(year,m)  # returns weekday of first day of the month and number of days in month
        sumDay+=mr[1] # days in month
    t=dt[1].split(':')
    tSec=int(t[2])
    tMin=int(t[1])
    tHour=int(t[0])
    timeSec=long(tSec+tMin*60+tHour*3600)
    return(timeSec+sumDay*3600*24)

def processFiles(currentPath,myDir):
    secPerRecord=60
    startTime=0
    reportTime=0
    installTime=0
    state=0
    numRecords=0
    #path=currentPath+'\\'+myDir+'\\'
    path=currentPath+'//'+myDir+'//'
    files = [ f for f in listdir(path) if isfile(join(path,f)) ]
    outFile=myDir+'.csv'
    print 'output file',outFile
    fout=open(outFile,'w')
     
    # write header
    fout.write('File,Sensor,tDays,Rec#,Temp,   X,   Y,   Z, Cnt, Max,Bins: (Low) to (High) \n')
    for f in files:
        try:
            (sensor,report)=getSensorReport(f)
            #print sensor,report

            fileName=path+f
            #print 'open file:',fileName
            with open(fileName,'r') as ff:
                doc= ff.readlines()

            line=doc[0].split('\r')
            index=0;   absTime=0;    state=0;
            while (index<len(line)):
                a=line[index].split(',')
                if 'Installed:' in a[0]:
                    b=a[0].split(':')
                    installTime=getInstallTime(b[1])
                if 'Secs per rec:' in a[0]:
                    b=a[0].split(':')
                    if len(b)==2:
                        secPerRecord=int(b[1],16)
                if 'Report date/time:' in a[0]:
                    reportTime=getAbsTime(a)
                   # print 'reportTime',reportTime-installTime
                if 'Start date/time:' in a[0]:
                    startTime=getAbsTime(a)
                    #print 'startTime',startTime-installTime
                if '# of recs:' in a[0]:
                    b=a[0].split(':')
                    if len(b)==2:
                        numRecords=int(b[1],16)
                        #print 'numRecords:',numRecords,a
                if a[0]=='Rec#':
                    state=1  # indicate a record starts on the next row
                if a[0]=='': # blank ends a record
                    state=0;
                index+=1    # go to the next row
                if state>0:
                    state+=1
                if state>SKIP_COUNT:  # record starting?
                    a=line[index].split(',')
                    if len(a)==DATA_COL:
                        recordNumber=int(a[0],16)
                        timeRecordSec=(recordNumber*secPerRecord)+startTime-installTime
                        timeRecordDay=timeRecordSec/(24.0*3600.0)
                        fout.write(f+','+sensor+','+str(timeRecordDay)+','+line[index]+'\n')
                    elif len(a)!=HEADER_COL and a[0]!='':
                        print 'BAD DATA LINE:',index,' FILE:',f,' MSG:',a
                        errorLogOut.write('BAD DATA in file: '+f+' LINE: '+str(index)+' MSG: '+a[0]+'\n')
                        #errorLogOut.write('BAD DATA in file: '+f+' LINE: '+str(index)+' MSG: '+a+'\n')
        except:
            print 'FILE FORMAT ERROR:',f
            errorLogOut.write('FILE FORMAT ERROR: '+f+'\n')
            
    fout.flush()
    fout.close()
    return;


################ main ##############
print 'start'
d=os.walk('.').next()[1]
print 'processing ', len(d)-1, 'files'
currentPath=os.getcwd()
print 'current path',currentPath
errorLogOut=open('ConsolidateErrorLog.txt','w') # error log file
errorLogOut.write('Consolidate Error Log for all files in directory: '+currentPath+'\n')
errorLogOut.write('Code Version: '+str(CODE_VERSION)+'\n')
for dd in d:
    if (dd!='Energy'):
        print '----------------------------------------------'
        print 'processing directory:',dd
        processFiles(currentPath,dd)
errorLogOut.write('Consolidate Error Log complete\n')
errorLogOut.flush()
errorLogOut.close()
print 'finished'  

