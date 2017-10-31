#!/bin/bash

IMAGEID=<insert-image-id>
INSTANCETYPE=t2.micro
SECURITYGROUP=<insert-security-group>
KEY=<insert-key-name>
SUBNET=<insert-subnet>

TAGKEY=<insert-tag-key>
TAGVALUE=<insert-key-value>

#######################
###  SCRIPT BEGINS   ##
#######################

###########################
# creates a new instance  #
###########################
result=$(sudo aws ec2 run-instances --image-id $IMAGEID --count 1 \
--instance-type $INSTANCETYPE --security-group-ids $SECURITYGROUP \
--key-name $KEY --monitoring Enabled=true --subnet-id $SUBNET)

############################
# add tag to new instance  #
############################
instance_id=$(echo $result | python -c \
        "import sys, json; print(json.load(sys.stdin)['Instances'][0]['InstanceId'])")

sudo aws ec2 create-tags --resources $instance_id --tags Key=$TAGKEY,Value=$TAGVALUE
