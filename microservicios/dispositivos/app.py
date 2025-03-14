from flask import Flask, request, jsonify
import psycopg2
import time
import random

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
                host="postgres-db",
                port=5432
            )
            print("✅ Conexión a PostgreSQL establecida (dispositivos)")
            return conn
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL (Intento {i+1}/10): {e}")
            time.sleep(5)
    raise Exception("🚨 No se pudo conectar a PostgreSQL después de 10 intentos")

# ✅ Registrar datos simulados desde el glucómetro
@app.route('/glucosa', methods=['POST'])
def registrar_glucosa():
    data = request.get_json()
    paciente_id = data.get('paciente_id')
    
    if not paciente_id:
        return jsonify({'error': 'Paciente ID es requerido'}), 400
    
    # Datos simulados
    tipo = "Glucómetro"
    nivel_glucosa = random.randint(70, 250)  # Nivel entre 70 y 250
    estado = "Normal" if nivel_glucosa <= UMBRAL_GLUCOSA else "Alerta"

    conn = get_db_connection()
    
    try:
        with conn.cursor() as cursor:
            # ✅ Insertar datos del dispositivo
            cursor.execute(
                "INSERT INTO dispositivos (tipo, estado, paciente_id) VALUES (%s, %s, %s) RETURNING id;",
                (tipo, estado, paciente_id)
            )
            dispositivo_id = cursor.fetchone()[0]
            conn.commit()

        # ✅ Si supera el umbral, enviar datos al microservicio de alertas
        if nivel_glucosa > UMBRAL_GLUCOSA:
            from requests import post
            alerta = {
                'mensaje': f"⚠️ Nivel de glucosa alto ({nivel_glucosa} mg/dL) para el paciente {paciente_id}",
                'paciente_id': paciente_id
            }
            post('http://alertas:5002/alertas', json=alerta)

        return jsonify({
            'message': 'Datos registrados correctamente',
            'dispositivo_id': dispositivo_id,
            'nivel_glucosa': nivel_glucosa,
            'estado': estado
        }), 201

    except Exception as e:
        print(f"❌ Error al registrar glucosa: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    finally:
        conn.close()

# ✅ Consultar datos de dispositivos registrados
@app.route('/dispositivos', methods=['GET'])
def obtener_dispositivos():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dispositivos;")
            dispositivos = cursor.fetchall()
            resultado = [{
                'id': dispositivo[0],
                'tipo': dispositivo[1],
                'estado': dispositivo[2],
                'paciente_id': dispositivo[3]
            } for dispositivo in dispositivos]

        return jsonify(resultado), 200

    except Exception as e:
        print(f"❌ Error al obtener dispositivos: {e}")
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
        print(f"❌ Error en health check: {e}")
        return jsonify({'status': 'error', 'details': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
