#!/usr/bin/env python3

import os
import sys
from confluent_kafka import Producer

BROKER = os.environ["KAFKA_BROKER"]

producer = Producer({"bootstrap.servers": BROKER})
producer.produce("email", sys.argv[1])
producer.poll(0)
producer.flush()
