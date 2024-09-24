#!/bin/bash


###Stop the Server 
#PID=` ps ax | grep plot_file_flas | grep -v grep | awk {'print $1'}`
#echo $PID

#kill -9 $PID

/bin/bash /home/CAHA/cp_CAHA_for_processing.sh

/bin/bash /home/CAHA/sensor_name_to_dir.sh
cd /home/CAHA/
/usr/bin/python /home/CAHA/Consolidate.py

cd /home/CAHA/
/usr/bin/python /home/CAHA/Analyze7.py

#nohup /usr/bin/python /home/flask/plot_file_flask_TurtleEnergy_V3.py > /dev/null 2>&1 </dev/null &



PID=` ps ax | grep plot_file_flas | grep -v grep | awk {'print $1'}`
echo $PID

kill -9 $PID
nohup /usr/bin/python /home/flask/plot_file_flask_TurtleEnergy_V4.py > /home/flask/plotter.log  2>&1  &

chgrp -R turtlewatch /home/CAHA

exit
