# consumer.py (Sin RabbitMQ)

import json
import smtplib

# ✅ Configurar correo SMTP (si vas a usar envío de alertas por correo)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL = 'tu-email@gmail.com'
PASSWORD = 'tu-password'

def enviar_email(alerta):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        mensaje = f"Alerta: Nivel de glucosa elevado para el paciente {alerta['paciente_id']}: {alerta['nivel_glucosa']}"
        server.sendmail(EMAIL, 'destinatario@gmail.com', mensaje)

# ✅ Función para simular alerta
def simular_alerta():
    data = {
        'paciente_id': 1,
        'nivel_glucosa': 250
    }
    print(f"⚠️ Alerta generada: {data}")
    enviar_email(data)

# ✅ Simulación directa (si lo necesitas)
if __name__ == "__main__":
    simular_alerta()
