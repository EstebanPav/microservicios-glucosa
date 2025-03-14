from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'alertas',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print('✅ Esperando alertas de Kafka...')

for message in consumer:
    data = message.value
    print(f"🚨 Alerta recibida desde Kafka: {data}")
