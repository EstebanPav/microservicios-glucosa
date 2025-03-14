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
                host="postgres-db",
                port=5432
            )
            print("✅ Conexión a PostgreSQL establecida")
            return conn
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL (Intento {i+1}/10): {e}")
            time.sleep(5)
    raise Exception("🚨 No se pudo conectar a PostgreSQL después de 10 intentos")

# ✅ Crear paciente
@app.route('/pacientes', methods=['POST'])
def create_paciente():
    try:
        data = request.get_json()
        if not data or 'nombre' not in data or 'edad' not in data or 'historial' not in data:
            return jsonify({'error': 'Datos inválidos'}), 400

        # ✅ Crear conexión por solicitud
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pacientes (nombre, edad, historial) VALUES (%s, %s, %s) RETURNING id;",
                (data['nombre'], data['edad'], data['historial'])
            )
            paciente_id = cursor.fetchone()[0]
            conn.commit()
        
        conn.close()

        return jsonify({'message': 'Paciente registrado', 'id': paciente_id}), 201
    except Exception as e:
        print(f"❌ Error al registrar paciente: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ✅ Obtener pacientes
@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    try:
        # ✅ Crear conexión por solicitud
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM pacientes;")
            pacientes = cursor.fetchall()

        conn.close()
        return jsonify(pacientes), 200
    except Exception as e:
        print(f"❌ Error al obtener pacientes: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ✅ Health check
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # ✅ Crear conexión por solicitud
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
        
        conn.close()
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return jsonify({'status': 'error', 'details': str(e)}), 500

# ✅ Cierre de conexión automático (si falla algo)
@app.teardown_appcontext
def close_connection(exception=None):
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            print("✅ Conexión a PostgreSQL cerrada")
    except Exception as e:
        print(f"❌ Error cerrando conexiones: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
