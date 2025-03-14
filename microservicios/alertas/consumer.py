from kafka import KafkaConsumer
import json

# ✅ Configurar KafkaConsumer
consumer = KafkaConsumer(
    'alertas',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print('✅ Esperando alertas de Kafka...')

for message in consumer:
    data = message.value
    alerta_id = data.get('id', 'N/A')
    mensaje = data.get('mensaje', 'N/A')
    paciente_id = data.get('paciente_id', 'N/A')
    
    print(f"🚨 Alerta recibida desde Kafka:")
    print(f"👉 ID: {alerta_id}")
    print(f"👉 Mensaje: {mensaje}")
    print(f"👉 Paciente ID: {paciente_id}")
