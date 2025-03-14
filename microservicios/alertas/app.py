from flask import Flask, request, jsonify
import psycopg2
import time

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
            print("✅ Conexión a PostgreSQL establecida (alertas)")
            return conn
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL (Intento {i+1}/10): {e}")
            time.sleep(5)
    raise Exception("🚨 No se pudo conectar a PostgreSQL después de 10 intentos")

# ✅ Crear alerta
@app.route('/alertas', methods=['POST'])
def create_alerta():
    data = request.get_json()
    if not data or 'mensaje' not in data or 'paciente_id' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO alertas (mensaje, paciente_id) VALUES (%s, %s) RETURNING id;",
                (data['mensaje'], data['paciente_id'])
            )
            conn.commit()

        return jsonify({'message': 'Alerta registrada'}), 201

    except Exception as e:
        print(f"❌ Error guardando alerta: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    finally:
        conn.close()

# ✅ Obtener alertas
@app.route('/alertas', methods=['GET'])
def get_alertas():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM alertas;")
            alertas = cursor.fetchall()
            resultado = [{
                'id': alerta[0],
                'mensaje': alerta[1],
                'fecha': alerta[2],
                'paciente_id': alerta[3]
            } for alerta in alertas]

        return jsonify(resultado), 200

    except Exception as e:
        print(f"❌ Error obteniendo alertas: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    finally:
        conn.close()

# ✅ Health check
@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'details': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
