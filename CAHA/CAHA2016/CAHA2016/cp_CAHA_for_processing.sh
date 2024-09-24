#!/bin/bash
echo "starting `basename "$0"`"   
FTPHOMEDIR="/home/u40427476-NWB"
TARGETDIR="/home/CAHA/received_activity_logs/"

#FORMAT
#2015-05-01_AA0007_t-12-01.txt -> mv to AA0007/2015-05-01_AA0007_t-12-01.txt
mkdir -p $TARGETDIR
cd $FTPHOMEDIR
for f in *.txt; do
        echo "Processing $f file." 
#        NEWDIRNAME=`echo $f | cut -d'_' -f 2`
#
#        FULLSTORAGEPATH=$TARGETBASEDIR/$NEWDIRNAME
#        mkdir -p $FULLSTORAGEPATH
#
#        echo "storage directory is $FULLSTORAGEPATH"

        cp $f $TARGETDIR
#        cp -n  $f $TARGETDIR
done
