#!/usr/bin/env bash

TOPIC_NAME=$1

$KAFKA_HOME/bin/kafka-topics.sh \
    --bootstrap-server $KAFKA_BROKER \
    --create \
    --topic $TOPIC_NAME \
    --partitions 1 \
    --replication-factor 1

$KAFKA_HOME/bin/kafka-topics.sh \
    --bootstrap-server $KAFKA_BROKER \
    --describe \
    --topic $TOPIC_NAME
