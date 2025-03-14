from flask import Flask, request, jsonify
import psycopg2
import time
from kafka import KafkaProducer
import json

app = Flask(__name__)

# ✅ Conexión a PostgreSQL
def get_db_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                dbname="glucosa_db",
                user="user",
                password="password",
                host="postgres-db",
                port=5432
            )
            return conn
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)
    raise Exception("🚨 Error de conexión")

# ✅ Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# ✅ Obtener alertas
@app.route('/alertas', methods=['GET'])
def get_alertas():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, mensaje, fecha, paciente_id FROM alertas;")
        alertas = cursor.fetchall()
        resultado = [{
            'id': alerta[0],
            'mensaje': alerta[1],
            'fecha': alerta[2].isoformat() if alerta[2] else None,
            'paciente_id': alerta[3]
        } for alerta in alertas]
    conn.close()
    return jsonify(resultado), 200

# ✅ Enviar alerta específica a Kafka
@app.route('/enviar-alerta', methods=['POST'])
def enviar_alerta():
    data = request.json
    if not data or 'id' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    # Obtener los datos de la alerta desde la base de datos
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, mensaje, fecha, paciente_id FROM alertas WHERE id = %s;", (data['id'],))
        alerta = cursor.fetchone()
    conn.close()

    if not alerta:
        return jsonify({'error': 'Alerta no encontrada'}), 404

    # ✅ Enviar alerta a Kafka
    payload = {
        'id': alerta[0],
        'mensaje': alerta[1],
        'fecha': alerta[2].isoformat() if alerta[2] else None,
        'paciente_id': alerta[3]
    }
    producer.send('alertas', payload)
    print(f"✅ Alerta enviada a Kafka: {payload}")
    
    return jsonify({'message': 'Alerta enviada a Kafka'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
