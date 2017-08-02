#!/bin/bash

ROOT_PATH=/root/yanbinwa/ansible

#stop and delete the original docker container
dockerRunContainer=`docker ps | grep -v "CONTAINER ID"`
if [ "$dockerRunContainer" != "" ]; then
	docker stop $(docker ps -q)
fi

dockerExistContainer=`docker ps -a -q | grep -v "CONTAINER ID"`
if [ "$dockerExistContainer" != "" ]; then
	docker rm $(docker ps -a -q)
fi
