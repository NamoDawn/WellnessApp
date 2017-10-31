#!/bin/bash

ENDTIME=$(date +%Y-%m-%dT%H:%M:%S)
STARTTIME=$(date -d "($ENDTIME) -5minutes" +%Y-%m-%dT%H:%M:%S)

#Getting the CPU Utilization
while read p; do

    CPUUTIL=$(aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \
        --dimensions Name=InstanceId,Value=i-093963f671ca141b5 --statistics Maximum \
        --start-time $STARTTIME --end-time $ENDTIME --period 360 | python -c \
        "import sys, json; print(json.load(sys.stdin)['Datapoints'][0]['Maximum'])")
    echo $CPUUTIL
done <instance_ip.txt
