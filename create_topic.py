from kafka.admin import KafkaAdminClient, NewTopic

# Настройки Kafka
KAFKA_BROKER = "kafka:9092"
TOPIC_NAME = "new_topic"

# Создание KafkaAdminClient
admin_client = KafkaAdminClient(
    bootstrap_servers=KAFKA_BROKER,
    client_id="admin_client"
)

# Создание нового топика
topic = NewTopic(
    name=TOPIC_NAME,
    num_partitions=1,
    replication_factor=1
)

try:
    admin_client.create_topics([topic])
    print(f"✅ Топик '{TOPIC_NAME}' успешно создан!")
except Exception as e:
    print(f"⚠️ Ошибка при создании топика: {e}")

admin_client.close()
