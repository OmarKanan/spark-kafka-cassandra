#!/usr/bin/env bash

nohup $KAFKA_HOME/bin/kafka-server-start.sh \
    $KAFKA_HOME/config/server.properties \
    --override zookeeper.connect=zookeeper:2181 \
    &

sleep 10
