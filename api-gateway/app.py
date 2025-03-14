from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

BASE_URL_PACIENTES = 'http://pacientes:5000'
BASE_URL_DISPOSITIVOS = 'http://dispositivos:5001'
BASE_URL_ALERTAS = 'http://alertas:5002'

# ✅ Función para hacer solicitudes con reintento automático
def make_request(method, url, json_data=None):
    max_retries = 5
    headers = {'Content-Type': 'application/json'} if json_data else {}

    for attempt in range(max_retries):
        try:
            response = requests.request(
                method,
                url,
                json=json_data if json_data else None,
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                return jsonify(response.json()), response.status_code
            else:
                print(f"⚠️ Error en la solicitud a {url}: {response.status_code} - {response.text}")
                return jsonify({'error': response.json()}), response.status_code
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Error de conexión ({attempt + 1}/{max_retries}) a {url}: {e}")
            time.sleep(2)
        except requests.exceptions.Timeout as e:
            print(f"❌ Tiempo de espera agotado ({attempt + 1}/{max_retries}) a {url}: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error desconocido ({attempt + 1}/{max_retries}) a {url}: {e}")
            time.sleep(2)
    
    return jsonify({'error': f'No se pudo conectar con {url} después de {max_retries} intentos'}), 500

# ✅ Endpoint para pacientes
@app.route('/pacientes', methods=['GET', 'POST'])
def pacientes():
    data = request.get_json()
    return make_request(request.method, f'{BASE_URL_PACIENTES}/pacientes', json_data=data)

# ✅ Endpoint para dispositivos
@app.route('/dispositivos', methods=['POST'])
def dispositivos():
    data = request.get_json()
    return make_request(request.method, f'{BASE_URL_DISPOSITIVOS}/glucosa', json_data=data)

# ✅ Endpoint para alertas
@app.route('/alertas', methods=['GET', 'POST'])
def alertas():
    data = request.get_json()
    return make_request(request.method, f'{BASE_URL_ALERTAS}/alertas', json_data=data)

# ✅ Health check
@app.route('/health', methods=['GET'])
def health_check():
    try:
        pacientes_status = requests.get(f"{BASE_URL_PACIENTES}/health").status_code
        dispositivos_status = requests.get(f"{BASE_URL_DISPOSITIVOS}/health").status_code
        alertas_status = requests.get(f"{BASE_URL_ALERTAS}/health").status_code
        
        status = {
            'pacientes': 'ok' if pacientes_status == 200 else 'error',
            'dispositivos': 'ok' if dispositivos_status == 200 else 'error',
            'alertas': 'ok' if alertas_status == 200 else 'error'
        }
        return jsonify({'status': 'ok', 'services': status}), 200
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return jsonify({'status': 'error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
