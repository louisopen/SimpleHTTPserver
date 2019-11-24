#!/bin/bash
#This bash called by autoboot.desktop or rootcron   #autoboot.desktop存放到/home/pi/.config/autostart/
#chmod =777 autoboot.desktop
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

python ./stats.py &

jump_dir=/home/pi/SimpleHTTPserver
cd $jump_dir
#tr -d "\r" < autorun.sh > newname.sh    #if you can't cd to .... just do this command. #置入新系統時若發生此訊息
#tr -d "\r" < autorun.sh > newname.sh    #if you got ...Syntax error: end of file unexpected (expecting "then")
pwd
sudo python3 $jump_dir/simple_webserver.py

cd /home/pi
exit 0