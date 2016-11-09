#!/bin/bash

root=`dirname $0`/..
source $root/venv/bin/activate
a=`lsof -i:9028`
if [ -z "$a" ];then
  echo "重启服务"
  cd $root/src
  nohup python manage.py runserver 9028 >> $root/logs/nohup.out &
else
  echo "服务已经在运行中，不需要再启动"
fi