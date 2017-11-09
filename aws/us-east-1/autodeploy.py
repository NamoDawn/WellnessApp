#!/usr/bin/python3
"""
full deployment
"""
import os
import time
from fabric.api import local, run, hosts, env, put, cd

env.hosts = ['54.211.234.124']

def install_dependencies():
    """ installing all the dependencies necessary for wellness app"""
    run("sudo apt-get update")
    run("sudo apt-get install -y nginx")
    run("sudo apt-get install -y python3-pip")
    run("sudo pip3 install gunicorn")
    run("sudo pip3 install pymysql")
    run("sudo pip3 install flask")
    run("sudo pip3 install flask-cors")
    run("sudo pip3 install passlib")
    run("sudo pip3 install pymysql")
    run("sudo apt-get install -y git")

def setup_nginx():
    """ setting up nginx"""
    run("sudo rm -f /etc/nginx/sites-available/default")

    run("sudo git -C /home/ubuntu clone https://github.com/NamoDawn/WellnessApp.git")
    put('wellness.conf', '/etc/init/', use_sudo=True)
    run("sudo chmod 755 /etc/nginx/sites-available/default")
    run("sudo service nginx restart")

def setup_upstart():
    """ configuring the upstart script"""
    run("sudo wget https://gist.githubusercontent.com/NamoDawn/0ce751fcdd44587d7e594128a1770450/raw/25da0c533eecac46de42d3ebc7f9972e13320f4e/wellness.conf -P /etc/init/")
    run("sudo chmod 755 /etc/init/wellness.conf")

def create_csv():
    run("sudo touch /home/ubuntu/WellnessApp/static/data/everything.csv")
    run("sudo chmod 777 /home/ubuntu/WellnessApp/static/data/everything.csv")
    run("sudo touch /home/ubuntu/WellnessApp/static/data/week.csv")
    run("sudo chmod 777 /home/ubuntu/WellnessApp/static/data/week.csv") 
    run("sudo touch /home/ubuntu/WellnessApp/static/data/month.csv")
    run("sudo chmod 777 /home/ubuntu/WellnessApp/static/data/month.csv")

def deploy():
    install_dependencies()
    setup_upstart()
    setup_nginx()
    with cd('/etc/init'):
        run('sudo start wellness')
    create_csv()
