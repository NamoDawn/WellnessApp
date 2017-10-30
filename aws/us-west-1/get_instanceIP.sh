#!/bin/bash


INSTANCENUM=$(sudo aws ec2 describe-instances --filters "Name=tag:instance-group,Values=wellness" | python -c "import sys, json; print(len(j\
son.load(sys.stdin)['Reservations']))")
#######################
## Instance IP Addr  ##
#######################
sudo truncate -s 0 instance_ip.txt
#Write instance public address to instance_ip.txt
for ((i=0;i<$INSTANCENUM;i+=1))
do
    instanceip=$(sudo aws ec2 describe-instances --filters "Name=tag:instance-group,Values=wellness" | python -c \
        "import sys, json; print(json.load(sys.stdin)['Reservations'][$i]['Instances'][0]['PublicIpAddress'])")
    echo $instanceip >> instance_ip.txt
done
