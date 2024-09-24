#!/bin/bash

#Directories
DATADIR='/home/CAHA/received_activity_logs'
TARGETBASEDIR="/home/CAHA"

#FORMAT
#2015-05-01_AA0007_t-12-01.txt -> mv to AA0007/2015-05-01_AA0007_t-12-01.txt
echo "Evaluate data file name"

cd $DATADIR

for f in *.txt; do
	echo "Processing $f file." 
	NEWDIRNAME=`echo $f | cut -d'_' -f 2`

	FULLSTORAGEPATH=$TARGETBASEDIR/$NEWDIRNAME
	mkdir -p $FULLSTORAGEPATH

	echo "storage directory is $FULLSTORAGEPATH"

	cp $f $FULLSTORAGEPATH 
	#cp -n  $f $FULLSTORAGEPATH 
done
