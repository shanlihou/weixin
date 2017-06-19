#/bin/sh
echo `ps -aux|grep 'python weixin.py'`
#pid=`ps -aux|grep 'python weixin.py'|awk '{print $2}'|head -1`
pid=`ps -aux|grep 'python weixin.py'|awk '{print $2}'`
echo $pid
for i in $pid
do 
    kill -9 $i
done
nohup python weixin.py &
