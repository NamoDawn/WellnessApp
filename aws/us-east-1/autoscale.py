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
        data=local("aws cloudwatch get-metric-statistics --namespace AWS/EC2 \
        --metric-name CPUUtilization --dimensions Name=InstanceId,Value={} \
        --statistics Maximum --start-time {} --end-time {} --period 60".format(instance_id, start_time, end_time),capture=True)
        try:
            print(len(json.loads(data)['Datapoints']))
            for i in range(len(json.loads(data)['Datapoints'])):
                max_val = json.loads(data).get('Datapoints')[i].get('Maximum')
                if max_val > max_util:
                    max_util = max_val
                    print(max_util)
            return max_util
        except:
            print(None)
    except:
        return None

def create_instance(image_id, instance_type, security_group, key, subnet, count=1):
    """ Created a new instance based on the required parameters passed in: see AWS Documentation for more info"""
    try:
        instance = local("aws ec2 run-instances --image-id {} --count {} \
        --instance-type {} --security-group-ids {} \
        --key-name {} --monitoring Enabled=true \
        --subnet-id {}".format(image_id, count, instance_type, security_group, key, subnet), capture=True)


        """ PENDING: deploy code here """

        return instance
    except:
        return None

def get_instance_id(instance):
    """ Retrieve an instance's ID with instance_info passed in"""
    return json.loads(instance).get("Instances")[0]['InstanceId']

def get_instance_info(instance_id):
    """ Retrieve all the information associated with an instance"""
    instance_info = local("sudo aws ec2 describe-instances \
    --instance-ids {}".format(instance_id), capture=True)
    return instance_info 

def get_instance_ip(instance_info):
    """ Retrieve an instance's IP with instance_info passed in"""
    return json.loads(instance_info).get("Reservations")[0].get("Instances")[0].get("PublicIpAddress")

def tag_instance(instance_id, key, val):
    """ Tag instance with a key/value pair by instance id"""
    local("sudo aws ec2 create-tags --resources {} --tags \
    Key={},Value={}".format(instance_id, key, val))    

def append_ip_to_haproxy(instance_ip):
    """ Appends a new ip address to the HAproxy config file"""
    local("echo '\tserver instance' {}':80 check' | sudo tee -a /etc/haproxy/haproxy.cfg".format(instance_ip))


def get_cluster_instanceID(cluster_key, cluster_value):
    """ Gets all the instances in a cluster"""
    instance_list = []
    existing_instance = []
    try:
        with open("cluster_instances.txt", 'r') as f:
            for line in f:
                existing_instance.append(line.strip("\n"))
    except:
        print(None)
    cluster_instances = local("aws ec2 describe-instances --filters \
    'Name=tag:{},Values={}'".format(cluster_key, cluster_value), capture=True)
    result = json.loads(cluster_instances).get('Reservations')

    local("sudo truncate -s 0 cluster_instances.txt")
    with open("cluster_instances.txt", 'a') as f:
        for i in range(len(result)):
            instance_list.append(result[i].get("Instances")[0].get("PublicIpAddress"))
            f.write(result[i].get("Instances")[0].get("PublicIpAddress"))

    """ new instances: scale up"""
    new_instances = (list(set(instance_list) - set(existing_instance)))
    if new_instances:
        for instance_ip in new_instances:
            append_ip_to_haproxy(instance_ip)
    local("sudo service haproxy reload")



def add_instance_to_target(target, cluster_key, cluster_value):
    """ add instance"""
    instance_list = []
    try:
        cluster_instances = local("aws ec2 describe-instances --filters \
        'Name=tag:{},Values={}'".format(cluster_key, cluster_value), capture=True)
    except:
        return None
    result = json.loads(cluster_instances).get('Reservations')
    for i in range(len(result)):
            instance_id = (result[i].get("Instances")[0].get("InstanceId"))
            try:
                local("aws elbv2 register-targets --target-group-arn {} \
                --targets Id={}".format(target, instance_id))
            except:
                continue

def autoscale():
    """ run methods here"""
    new_instance = create_instance("ami-7dce6507", "t2.micro", "sg-56949f24", "virginia-personal","subnet-af38da80", 1)
    new_instance_id = get_instance_id(new_instance)
    tag_instance(new_instance_id, "instance-group", "wellness")
    new_instance_info = get_instance_info(new_instance_id)
    new_instance_ip = get_instance_ip(new_instance_info)

def add_all_instances_to_target():
    add_instance_to_target("arn:aws:elasticloadbalancing:us-east-1:137086037822:targetgroup/wellness-target-group/9c8e0b13a636e49d", "instance-group", "wellness")
