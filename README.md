### Using Docker containers:
- Manually send messages to Kafka topics using Python tools.
- Spark Streaming consumes Kafka topics and writes to Cassandra tables.

## How to run

#### Launch containers
~~~
docker compose up -d
~~~

#### Create Cassandra tables
Attach to cassandra container, then:
~~~
./setup.sh
~~~
Connection will fail several times until Cassandra is ready.

#### Launch Spark streaming job
Attach to spark container, then:
~~~
./stream.sh
~~~

#### Launch Python requests
Attach to python container, then:
~~~
./send_email.py email@example.com
./send_otp.py email@example.com 123456
~~~

#### Check Cassandra tables
Attach to cassandra container, then connect to cluster:
~~~
cqlsh
~~~
Then check tables:
~~~sql
select * from test.users;
select * from test.valid;
~~~
