#!/usr/bin/env bash

TOPIC_NAME=$1

$KAFKA_HOME/bin/kafka-topics.sh \
    --bootstrap-server $KAFKA_BROKER \
    --delete \
    --topic $TOPIC_NAME

echo Deleted topic $TOPIC_NAME