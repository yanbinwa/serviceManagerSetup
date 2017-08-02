#!/bin/bash

ROOT_PATH=/root/yanbinwa/ansible

MANIFEST_FILE_PATH=$1

DELETE_ALL_DOCKER=$2

if [ "$MANIFEST_FILE_PATH" = "" ]; then
	echo "MANIFEST_FILE_PATH is empty"
	exit -1;
fi

if [ "$DELETE_ALL_DOCKER" = "true" ]; then
	/bin/bash $ROOT_PATH/script/uninstallAll.sh
fi
 
#remove the old target
rm -rf $ROOT_PATH/target/*

#read the manifest file to build the host template
python $ROOT_PATH/script/serviceManagerSetup.py $MANIFEST_FILE_PATH

#create docker container
/bin/bash $ROOT_PATH/target/docker/docker_container.sh

#run ansible script
ansible-playbook $ROOT_PATH/target/ansible/main.yaml -i $ROOT_PATH/target/ansible/host.template
