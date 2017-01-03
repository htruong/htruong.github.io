#!/bin/sh

cd /home/pi/htruong.github.io

while true
do
	client=`mosquitto_sub -h iot.tnhh.net -t '/site/tnhh.net/compile/' -C 2`
	git pull
	git checkout source
	rake publish
	sleep 30
done
