from flask import Flask, request, jsonify
import psycopg2
import time
from kafka import KafkaProducer
import json

app = Flask(__name__)

# ✅ Función para conectar a PostgreSQL
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
            print("✅ Conexión a PostgreSQL establecida")
            return conn
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL (Intento {i+1}/10): {e}")
            time.sleep(5)
    raise Exception("🚨 No se pudo conectar a PostgreSQL después de 10 intentos")

conn = get_db_connection()

# ✅ Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# ✅ Crear alerta en la base de datos (SIN enviar a Kafka todavía)
@app.route('/alertas', methods=['POST'])
def create_alerta():
    data = request.json

    if not data or 'mensaje' not in data or 'paciente_id' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO alertas (mensaje, paciente_id) VALUES (%s, %s) RETURNING id;",
                (data['mensaje'], data['paciente_id'])
            )
            alerta_id = cursor.fetchone()[0]
            conn.commit()

        print(f"✅ Alerta registrada en la base de datos: {data}")
        return jsonify({'message': 'Alerta registrada', 'id': alerta_id}), 201

    except Exception as e:
        print(f"❌ Error guardando alerta en la base de datos: {e}")
        return jsonify({'error': 'Error guardando la alerta'}), 500

# ✅ Nueva ruta para enviar alerta a Kafka MANUALMENTE
@app.route('/enviar-alerta', methods=['POST'])
def enviar_alerta():
    data = request.json

    alerta_id = data.get('id')
    if not alerta_id:
        return jsonify({'error': 'ID de alerta requerido'}), 400

    try:
        # ✅ Buscar la alerta en la base de datos por ID
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, mensaje, paciente_id FROM alertas WHERE id = %s;",
                (alerta_id,)
            )
            alerta = cursor.fetchone()

            if not alerta:
                return jsonify({'error': 'Alerta no encontrada'}), 404

            alerta_data = {
                'id': alerta[0],
                'mensaje': alerta[1],
                'paciente_id': alerta[2]
            }

            # ✅ Enviar alerta a Kafka
            producer.send('alertas', value=alerta_data)
            producer.flush()
            print(f"✅ Alerta enviada a Kafka: {alerta_data}")

        return jsonify({'message': 'Alerta enviada a Kafka'}), 200

    except Exception as e:
        print(f"❌ Error enviando alerta a Kafka: {e}")
        return jsonify({'error': 'Error enviando alerta'}), 500

# ✅ Obtener alertas
@app.route('/alertas', methods=['GET'])
def get_alertas():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, mensaje, paciente_id FROM alertas;")
            alertas = cursor.fetchall()

            # ✅ Convertir la respuesta en una lista de objetos
            resultado = [{
                'id': alerta[0],
                'mensaje': alerta[1],
                'paciente_id': alerta[2]
            } for alerta in alertas]

            return jsonify(resultado), 200

    except Exception as e:
        print(f"❌ Error obteniendo alertas: {e}")
        return jsonify({'error': 'Error obteniendo alertas'}), 500

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, mensaje, paciente_id FROM alertas;")
            alertas = cursor.fetchall()

            resultado = [{
                'id': alerta[0],
                'mensaje': alerta[1],
                'paciente_id': alerta[2]
            } for alerta in alertas]

            return jsonify(resultado), 200

    except Exception as e:
        print(f"❌ Error obteniendo alertas: {e}")
        return jsonify({'error': 'Error obteniendo alertas'}), 500

# ✅ Health Check
@app.route('/health', methods=['GET'])
def health_check():
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return jsonify({'status': 'error', 'details': str(e)}), 500

# ✅ Cierre de conexiones
@app.teardown_appcontext
def close_connection(exception=None):
    if conn:
        conn.close()
        print("✅ Conexión a PostgreSQL cerrada")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
