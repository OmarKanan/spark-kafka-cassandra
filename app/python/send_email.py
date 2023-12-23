import os
import sys
from confluent_kafka import Producer

TOPIC = os.environ["KAFKA_TOPIC_EMAIL"]
BROKER = os.environ["KAFKA_BROKER"]

producer = Producer({"bootstrap.servers": BROKER})
producer.produce(TOPIC, sys.argv[1])
producer.poll(0)
producer.flush()
