#!/usr/bin/env bash

TOPIC_NAME=$1

NUM_PARTITIONS=$(
    $KAFKA_HOME/bin/kafka-topics.sh \
        --bootstrap-server $KAFKA_BROKER \
        --describe \
        --topic $TOPIC_NAME \
        | awk '{print $6}' | head -n 1
)

echo Number of partitions in topic $TOPIC_NAME: $NUM_PARTITIONS
