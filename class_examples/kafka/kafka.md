# HANDS ON WITH KAFKA

- Start the docker-compose
```bash
docker compose up -d 
```
create a new topic

```bash
docker exec kafka-docker-kafka-1   kafka-topics.sh --create --topic test -partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
```
list all topics
```bash
docker exec kafka-docker-kafka-1   kafka-topics.sh --list --bootstrap-server localhost:9092
```

describe a topic

```bash
docker exec  kafka-docker-kafka-1  kafka-topics.sh --describe --topic test --bootstrap-server localhost:9092
```

delete a topic

```bash
docker exec  kafka-docker-kafka-1  kafka-topics.sh --delete --topic test --bootstrap-server localhost:9092
```

build producer docker

```bash
docker build -t kafka-producer .
```

run producer

```bash
docker run --network=host --name producer kafka-producer 
```

build the consumer
```bash
docker build -t kafka-consumer .
```

run the consumer
```bash
docker run --network=host --name consumer2 kafka-consumer
```

describe the consumer groups
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group my-group
```
