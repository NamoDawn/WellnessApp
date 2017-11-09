# Stow
This project contains functions for autoscaling and auto deployment through the AWS CLI
## Getting Started

## Requirements
### Ubuntu Machine
You can use last version of Ubuntu or any other OS 
(Note: unit test done on Ubuntu 14.04).

## Requirements for the Wellness App
The following are the primary dependencies for running the Wellness app

### MySQL 5.7

```
$ wget http://dev.mysql.com/get/mysql-apt-config_0.6.0-1_all.deb # From https://dev.mysql.com/downloads/repo/apt/
$ sudo dpkg -i mysql-apt-*.deb
$ sudo apt-get update
$ sudo apt-get install mysql-server
```
### Nginx

```
~$ sudo apt-get install nginx
```

### Pip3
```
~$ sudo apt-get install python3-pip
```

### passlib (1.7.1)
```
~$ pip3 install passlib
```

### Flask-Cors (3.0.3)
```
~$ pip3 install flask_cors
```

### PyMySQL (0.7.11)
```
~$ pip3 install pymysql
```

### gunicorn (19.7.1) 
```
~$ pip3 install gunicorn
```

## Requirements for the AWS Scaling and Deployment
### Pip3
```
~$ sudo apt-get install python3-pip
```
### AWS CLI
```
~$ pip3 install awscli
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

* More information available in the aws directory

### Setup

#### Setting up MySQL
```
~$ mysql -h<hostname> -u<user> wellness_dev_db < setup_scripts/wellness_db_setup.sql
~$ mysql -h<hostname> -u<user> wellness_dev_db < setup_scripts/wellness_table_setup.sql
```

## Author(s)
* Naomi Sorrell
* Stuart Kuredjian
* Lisa Leung 
