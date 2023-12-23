import os
import random
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from cassandra.cluster import Cluster

KAFKA_BROKER = os.environ["KAFKA_BROKER"]
CASSANDRA_KEYSPACE = os.environ["CASSANDRA_KEYSPACE"]
CASSANDRA_TABLE_USERS = os.environ["CASSANDRA_TABLE_USERS"]
CASSANDRA_TABLE_VALID = os.environ["CASSANDRA_TABLE_VALID"]
    
def generateOtp():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))

def checkOtp(email, otp):
    cassandra = Cluster(['cassandra']).connect(CASSANDRA_KEYSPACE)
    rows = cassandra.execute(f"select otp from users where email = '{email}'")
    if not rows:
        return False
    return int(rows[0].otp) == int(otp)

spark = SparkSession.builder \
    .appName("KafkaStructuredStreaming") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

users = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("startingOffsets", "latest") \
    .option("subscribe", "email") \
    .load() \
    .selectExpr("cast(value as string) as email") \
    .withColumn("otp", udf(generateOtp)()) \
    .writeStream \
    .queryName("email") \
    .outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", CASSANDRA_KEYSPACE) \
    .option("table", CASSANDRA_TABLE_USERS) \
    .start()

valid = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("startingOffsets", "latest") \
    .option("subscribe", "otp") \
    .load() \
    .selectExpr("cast(value as string) as values", "timestamp as ts") \
    .withColumn("email", split(col("values"), ",").getItem(0)) \
    .withColumn("otp", split(col("values"), ",").getItem(1)) \
    .withColumn("valid", udf(checkOtp)(col("email"), col("otp"))) \
    .select("email", "ts", "valid") \
    .writeStream \
    .queryName("valid") \
    .outputMode("append") \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", CASSANDRA_KEYSPACE) \
    .option("table", CASSANDRA_TABLE_VALID) \
    .start()

users.awaitTermination()
valid.awaitTermination()
