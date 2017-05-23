#!/bin/sh
docker run -i -t -d --net yanbin -p 8091:8091 --ip 172.18.0.21 --name orchestration_active ubuntu:v2 /bin/bash
docker run -i -t -d --net yanbin -p 2191:2191 --ip 172.18.0.11 --name zookeeper_1 ubuntu:v2 /bin/bash
docker run -i -t -d --net yanbin -p 2192:2192 --ip 172.18.0.12 --name zookeeper_2 ubuntu:v2 /bin/bash
docker run -i -t -d --net yanbin -p 2193:2193 --ip 172.18.0.13 --name zookeeper_3 ubuntu:v2 /bin/bash
docker run -i -t -d --net yanbin -p 8101:8101 --ip 172.18.0.31 --name collection_A ubuntu:v2 /bin/bash
docker run -i -t -d --net yanbin -p 8103:8103 --ip 172.18.0.33 --name collection_C ubuntu:v2 /bin/bash
docker run -i -t -d --net yanbin -p 8102:8102 --ip 172.18.0.32 --name collection_B ubuntu:v2 /bin/bash
docker run -i -t -d --net yanbin -p 8092:8092 --ip 172.18.0.22 --name orchestration_standby ubuntu:v2 /bin/bash
