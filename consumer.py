from kafka import KafkaConsumer
import json


KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "test_topic"


consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my_consumer_group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)


for message in consumer:
    print(message.value)
