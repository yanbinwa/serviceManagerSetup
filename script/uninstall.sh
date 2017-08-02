#!/bin/bash

DEL_SERVICE_NAME_LIST_STR=$1

if [ "$DEL_SERVICE_NAME_LIST_STR" = "" ]; then
    exit 0
fi

serviceNameList=${DEL_SERVICE_NAME_LIST_STR//,/ }
for serviceName in $serviceNameList
do
    containerId=`docker ps | grep $serviceName | awk '{print $1}'`
    if [ "$containerId" != "" ]; then
    	docker stop $containerId
    	docker rm $containerId
    fi
done