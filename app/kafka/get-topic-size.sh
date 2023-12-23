#!/usr/bin/env bash

TOPIC_NAME=$1

SIZE=$(
    $KAFKA_HOME/bin/kafka-run-class.sh kafka.tools.GetOffsetShell \
        --broker-list $KAFKA_BROKER \
        --topic $TOPIC_NAME \
        | awk -F  ":" '{sum += $3} END {print sum}'
)

echo Size of topic $TOPIC_NAME: $SIZE
