#!/usr/bin/python3
"""
full deployment
"""
import os
import time
from fabric.api import local, run, hosts, env, put

env.hosts = []

def install_dependencies():
    run("sudo apt-get update")
    run("sudo apt-get install -y nginx")
    run("sudo service nginx restart")
    run("sudo apt-get install -y gunicorn")
    run("sudo apt-get install -y python3-pip")
    run("sudo apt-get install -y git")
    run("sudo pip3 install pymysql")
    run("sudo pip3 install flask")
    run("sudo pip3 install flask-cors")
    run("sudo apt-get install -y python-pip")
    run("sudo pip install flask-cors")
    run("sudo pip install passlib")
    run("sudo pip install pymysql")
    run("sudo rm /etc/nginx/sites-available/default")
    run("sudo git clone https://github.com/NamoDawn/WellnessApp.git /home/ubuntu")
    run("sudo wget https://gist.githubusercontent.com/NamoDawn/be33e53528e4cf3001f6e3b1f53ad3ef/raw/845f0cd3af78a5b7e2c11ddbc6c345a08deb9232/default -P /etc/nginx/sites-available/")
    run("sudo chmod 755 /etc/nginx/sites-available/default")
    run("sudo wget https://gist.githubusercontent.com/NamoDawn/0ce751fcdd44587d7e594128a1770450/raw/8647dcd2793d9cd891182406c18ae89c7fd89b53/wellness.conf -P /etc/init/")
    run("sudo chmod 755 /etc/init/wellness.conf")
    run("sudo start /etc/init/wellness")
    run("sudo service nginx restart")
