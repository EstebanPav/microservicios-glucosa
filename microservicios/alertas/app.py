from flask import Flask, request, jsonify
import psycopg2
import time

app = Flask(__name__)

# ✅ Función para conectar a PostgreSQL con reintento automático
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

# ✅ Crear conexión inicial a PostgreSQL
conn = get_db_connection()

# ✅ Crear alerta
@app.route('/alertas', methods=['POST'])
def create_alerta():
    data = request.json

    # ✅ Validación de datos recibidos
    if not data or 'mensaje' not in data or 'paciente_id' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    try:
        # ✅ Guardar alerta en la base de datos
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO alertas (mensaje, paciente_id) VALUES (%s, %s) RETURNING id;",
                (data['mensaje'], data['paciente_id'])
            )
            conn.commit()

        print(f"✅ Alerta guardada en la base de datos: {data}")
        return jsonify({'message': 'Alerta registrada'}), 201

    except Exception as e:
        print(f"❌ Error guardando alerta en la base de datos: {e}")
        return jsonify({'error': 'Error guardando la alerta'}), 500

# ✅ Obtener todas las alertas
@app.route('/alertas', methods=['GET'])
def get_alertas():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM alertas;")
            alertas = cursor.fetchall()
            return jsonify(alertas), 200
    except Exception as e:
        print(f"❌ Error obteniendo alertas: {e}")
        return jsonify({'error': 'Error obteniendo alertas'}), 500

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
    try:
        if conn:
            conn.close()
            print("✅ Conexión a PostgreSQL cerrada")
    except Exception as e:
        print(f"❌ Error cerrando conexiones: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
