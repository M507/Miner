#!/bin/bash


FILE=/var/www/html/START_RDP_SESSION.env

echo "1" > $FILE

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "0" > $FILE
fi

cat $FILE