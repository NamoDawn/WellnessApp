#!/bin/bash
#This script gets instanceid and instance public ip address
# and writes it to instance_id.txt and instance_ip.txt, respectively

# Getting the number of instances
INSTANCENUM=$(sudo aws ec2 describe-instances --filters "Name=tag:instance-group,Values=wellness" | python -c "import sys, json; print(len(json.load(sys.stdin)['Reservations']))")

#######################
##     Instance ID   ##
#######################
#Clear instance_id.txt
sudo truncate -s 0 instance_id.txt

#Write instance ids to instance_id.txt
for ((i=0;i<$INSTANCENUM;i+=1))
do
    instanceid=$(sudo aws ec2 describe-instances --filters "Name=tag:instance-group,Values=wellness" | python -c \
	"import sys, json; print(json.load(sys.stdin)['Reservations'][$i]['Instances'][0]['InstanceId'])")
    echo $instanceid >> instance_id.txt
done


#######################
## Instance IP Addr  ##
#######################

#Write instance public address to instance_ip.txt
for ((i=0;i<$INSTANCENUM;i+=1))
do
    instanceip=$(sudo aws ec2 describe-instances --filters "Name=tag:instance-group,Values=wellness" | python -c \
        "import sys, json; print(json.load(sys.stdin)['Reservations'][$i]['Instances'][0]['PublicIpAddress'])")
    echo $instanceip >> instance_ip.txt
done
