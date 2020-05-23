#!/bin/bash
      while true

        do

        tomcat_id=`ps -ef | grep python3 | grep -v grep | awk '{print $2}'`
echo $tomcat_id

for id in $tomcat_id
do
    kill -9 $id
    echo "killed $id"
done

`screen`
`python3 /home/python/bussise/app.py`

        sleep 20000

        done

