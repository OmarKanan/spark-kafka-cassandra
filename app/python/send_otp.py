import os
import sys
from confluent_kafka import Producer

TOPIC = os.environ["KAFKA_TOPIC_OTP"]
BROKER = os.environ["KAFKA_BROKER"]

producer = Producer({"bootstrap.servers": BROKER})
producer.produce(TOPIC, f"{sys.argv[1]},{sys.argv[2]}")
producer.poll(0)
producer.flush()
