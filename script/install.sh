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

#read the manifest file to build the host template
python $ROOT_PATH/script/serviceManagerSetup.py $ROOT_PATH/conf/manifest1.yml

#create docker container
sh $ROOT_PATH/target/docker/docker_container.sh

#run ansible script
ansible-playbook $ROOT_PATH/target/ansible/main.yaml -i $ROOT_PATH/target/ansible/host.template