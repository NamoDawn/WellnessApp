#!/usr/bin/python3
"""
    Fabric script that automatically scale AWS instances
"""
from fabric.api import local, sudo
import datetime
import json
import time

def get_metrics(instance_id):
    """ Retrieves the CPU Utilization of an instance"""
    """ Check maximum val for the utilizationin the last 5 minutes"""
    end_time = time.strftime("%Y-%m-%dT%H:%M:%S")
    start_time = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S")
    max_util = 0.0

    try:
        data=local("sudo aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value={} --statistics Maximum --start-time {} --end-time {} --period 60".format(instance_id, start_time, end_time),capture=True)
        try:
            for i in range(len(json.loads(data)['Datapoints'])):
                max_val = json.loads(data).get('Datapoints')[i].get('Maximum')
                if max_val > max_util:
                    max_util = max_val
            return max_util
        except:
            return None

    except:
        return None


def create_instance(image_id, instance_type, security_group, key, subnet, instance_key, instance_value):
    """ Created a new instance based on the required parameters passed in: see AWS Documentation for more info"""
    try:
        instance = local("sudo aws ec2 run-instances --image-id {} --count 1 \
        --instance-type {} --security-group-ids {} \
        --key-name {} --monitoring Enabled=true --subnet-id {}".format(image_id, instance_type, security_group, key, subnet), capture=True)

        """ For us-east-1"""
        """ add tag for instance"""
        new_instance_id = json.loads(instance).get("Instances")[0]['InstanceId']
        local("sudo aws ec2 create-tags --resources {} --tags Key={},Value={}".format(new_instance_id, instance_key, instance_value))


        new_instance_info = local("sudo aws ec2 describe-instances --instance-ids {}".format(new_instance_id), capture=True)
        new_instance_ip = json.loads(new_instance_info).get("Reservations")[0].get("Instances")[0].get("PublicIpAddress")

        """ PENDING: deploy code here """

        """ Update HAProxy"""
        append_ip_to_haproxy(new_instance_ip)
    except:
        return None

def append_ip_to_haproxy(instance_id):
    """ Appends a new ip address to the HAproxy config file"""
    local("echo '\tserver instance' {}':80 check' | sudo tee -a /etc/haproxy/haproxy.cfg".format(instance_id))
    local("sudo service haproxy reload")
