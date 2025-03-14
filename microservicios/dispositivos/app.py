from flask import Flask, request, jsonify
import psycopg2
import time

app = Flask(__name__)

# 🚨 Umbral para generar alerta
UMBRAL_GLUCOSA = 180

# ✅ Función para conectar a PostgreSQL
def get_db_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                dbname="glucosa_db",
                user="user",
                password="password",
                host="postgres-db"
            )
            print("✅ Conexión a PostgreSQL establecida")
            return conn
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL: {e}")
            time.sleep(5)
    raise Exception("🚨 No se pudo conectar a PostgreSQL después de 10 intentos")

conn = get_db_connection()

@app.route('/glucosa', methods=['POST'])
def recibir_glucosa():
    data = request.json
    paciente_id = data.get('paciente_id')
    nivel_glucosa = data.get('nivel_glucosa')
    hora = data.get('hora')

    if not paciente_id or not nivel_glucosa or not hora:
        return jsonify({'error': 'Datos inválidos'}), 400

    try:
        if nivel_glucosa > UMBRAL_GLUCOSA:
            mensaje = f"⚠️ Nivel de glucosa alto ({nivel_glucosa} mg/dL) para el paciente {paciente_id}"

            # ✅ Guardar alerta en la base de datos
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO alertas (mensaje, paciente_id) VALUES (%s, %s) RETURNING id;",
                    (mensaje, paciente_id)
                )
                conn.commit()

            print(f"✅ Alerta generada: {mensaje}")

            return jsonify({'message': 'Alerta generada'}), 200
        else:
            return jsonify({'message': 'Nivel de glucosa normal'}), 200
    except Exception as e:
        print(f"❌ Error procesando datos: {e}")
        return jsonify({'error': 'Error procesando datos'}), 500

# ✅ Health check para PostgreSQL
@app.route('/health', methods=['GET'])
def health_check():
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return jsonify({'status': 'error', 'details': str(e)}), 500

# ✅ Cierre de conexiones para liberar recursos
@app.teardown_appcontext
def close_connection(exception=None):
    if conn:
        conn.close()
        print("✅ Conexión a PostgreSQL cerrada")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
