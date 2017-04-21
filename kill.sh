#/bin/sh
pid=`ps -aux|grep 'python weixin.py'|awk '{print $2}'|head -1`
kill -9 $pid
