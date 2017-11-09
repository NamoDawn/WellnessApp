#!/usr/bin/python3
"""
full deployment
"""
import os
import time
from fabric.api import local, run, hosts, env, put, cd

env.hosts = ['34.226.154.101']

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

def add_project():
    run("sudo git -C /home/ubuntu clone https://github.com/NamoDawn/WellnessApp.git")


def setup_nginx():
    """ setting up nginx"""
    run("sudo rm -f /etc/nginx/sites-available/default")
    run("sudo wget https://gist.githubusercontent.com/NamoDawn/be33e53528e4cf3001f6e3b1f53ad3ef/raw/845f0cd3af78a5b7e2c11ddbc6c345a08deb9232/default -P /etc/nginx/sites-available/")
    run("sudo chmod 755 /etc/nginx/sites-available/default")
    run("sudo service nginx restart")

def setup_upstart():
    """ configuring the upstart script"""
    put('wellness.conf', '/etc/init/', use_sudo=True)
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
    add_project()
    setup_upstart()
    setup_nginx()
    with cd('/etc/init'):
        run('sudo start wellness')
    create_csv()
