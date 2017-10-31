#!/bin/bash

#Rewrite the base configuration for haproxy.cfg
echo "global
        log /dev/log    local0
        log /dev/log    local1 notice
        maxconn 4096
        chroot /var/lib/haproxy
        user haproxy
        group haproxy
        daemon

defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        contimeout 5000
        clitimeout 50000
        srvtimeout 50000
        errorfile 400 /etc/haproxy/errors/400.http
        errorfile 403 /etc/haproxy/errors/403.http
        errorfile 408 /etc/haproxy/errors/408.http
        errorfile 500 /etc/haproxy/errors/500.http
        errorfile 502 /etc/haproxy/errors/502.http
        errorfile 503 /etc/haproxy/errors/503.http
        errorfile 504 /etc/haproxy/errors/504.http

mode http
        option forwardfor
        option http-server-close

frontend www-http
        bind 0.0.0.0:80
        reqadd X-Forwarded-Proto:\ http
        default_backend www-backend

backend www-backend
        balance roundrobin" | sudo tee /etc/haproxy/haproxy.cfg

#Take the Public IP address from tmp.txt retrieved from aws cli on all instances-group=wellness
while read p; do
    echo $'\tserver instance' $p':80 check' | sudo tee -a /etc/haproxy/haproxy.cfg
done <instance_ip.txt

#Reload haproxy
sudo service haproxy reload
