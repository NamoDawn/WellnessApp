# Automatic Scaling and Deployment with AWS
This project contains functions for autoscaling and auto deployment through the AWS CLI
## Getting Started

## Requirements
### Ubuntu Machine
You can use last version of Ubuntu or any other OS 
(Note: unit test done on Ubuntu 14.04 ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-20170727 (ami-841f46ff), available through AWS).

### Pip
Install Pip 
```
sudo apt-get install python-pip python-dev
```

### AWS CLI
```
pip install awscli --upgrade --user
```

#### Configure AWS
Configure your settings for the [aws cli](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).  Note that we currently only have tests in the regions us-west-1 and us-east-1 because certain aws commands are available in these two regions
```
~$ aws configure
AWS Access Key ID: <add access key> 
AWS Secret Access Key: <add secret access key>
Default region name: us-east-1
Default output format [json]: json
```


## Files
There are Fabric files that condenses all aws calls for automatic scaling and deployment

|   **Name**    |  **Description** |
|---------------|----------------|
|**autoscale.py**|    This is a fabric file that contains all the methods for automatics scaling of EC2 instances      |
|**bash_scripts/config_haproxy.sh**|     Stand alone script for configuring haproxy    |
|**bash_scripts/create_instance.sh**|     Stand alone aws script for creating EC2 instances   |
|**bash_scripts/get_instanceIP.sh**|     Stand alone aws script for getting an EC2 instance's IP address  |
|**bash_scripts/get_metrics.sh**|     Stand alone aws script for getting an EC2 instance's metrics  |
|**bash_scripts/write_instances.sh**|    This script gets instanceid and instance public ip address and writes it to instance_id.txt and instance_ip.txt, respectively   |


## Resource(s)
* [Getting started with AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)
* [Working with AWS Services](http://docs.aws.amazon.com/cli/latest/userguide/chap-working-with-services.html)
* [Using Amazon EC2 instances](http://docs.aws.amazon.com/cli/latest/userguide/cli-ec2-launch.html)
* [BoTo3](https://boto3.readthedocs.io/en/latest/reference/services/autoscaling.html)

## Author(s)
* Lisa Leung 
