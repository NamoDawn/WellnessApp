#!/bin/bash

TAGKEY=<key>
TAGVALUE=<value>

sudo aws ec2 describe-instances --filters "Name=tag:$TAGKEY,Values=$TAGVALUE" | grep PublicIpAddress | cut -d ":" -f 2 | cut -d\
 "," -f1 | tr -d '"' | cut -d " " -f 2 > instance_ip.txt
