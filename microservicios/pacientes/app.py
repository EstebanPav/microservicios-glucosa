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

# ✅ Leer pacientes
@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre, edad, historial FROM pacientes;")
            pacientes = cursor.fetchall()

        conn.close()

        pacientes_json = [
            {'id': p[0], 'nombre': p[1], 'edad': p[2], 'historial': p[3]} for p in pacientes
        ]

        return jsonify(pacientes_json), 200
    except Exception as e:
        print(f"❌ Error al obtener pacientes: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ✅ Actualizar paciente
@app.route('/pacientes/<int:id>', methods=['PUT'])
def update_paciente(id):
    try:
        data = request.get_json()
        if not data or 'nombre' not in data or 'edad' not in data or 'historial' not in data:
            return jsonify({'error': 'Datos inválidos'}), 400

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE pacientes SET nombre = %s, edad = %s, historial = %s WHERE id = %s RETURNING id;",
                (data['nombre'], data['edad'], data['historial'], id)
            )
            updated_id = cursor.fetchone()
            if not updated_id:
                return jsonify({'error': 'Paciente no encontrado'}), 404
            conn.commit()

        conn.close()

        return jsonify({'message': 'Paciente actualizado', 'id': id}), 200
    except Exception as e:
        print(f"❌ Error al actualizar paciente: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ✅ Eliminar paciente
@app.route('/pacientes/<int:id>', methods=['DELETE'])
def delete_paciente(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM pacientes WHERE id = %s RETURNING id;", (id,))
            deleted_id = cursor.fetchone()
            if not deleted_id:
                return jsonify({'error': 'Paciente no encontrado'}), 404
            conn.commit()

        conn.close()

        return jsonify({'message': 'Paciente eliminado'}), 200
    except Exception as e:
        print(f"❌ Error al eliminar paciente: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ✅ Health check
@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
        conn.close()
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return jsonify({'status': 'error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
