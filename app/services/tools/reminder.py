import datetime
import json
import os
import requests


BASE_URL = os.getenv("BASE_URL")
WHATSAPP_URL = os.getenv("WHATSAPP_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def lambda_handler(event, context):
    enviar_recordatorio()
    return {
        "statusCode": 200,
        "body": json.dumps("Recordatorios enviados con éxito")
    }


def enviar_recordatorio():
    """
    Esta función se ejecuta a la hora programada y envía un recordatorio
    con los turnos para el próximo día.
    """

    dia_siguiente = datetime.date.today() + datetime.timedelta(days=1)
    
    turnos = obtener_turnos_para_dia(dia_siguiente)

    for turno in turnos:
        
        try:
            reply_data = recordatorio_template(turno["telefono"], turno)
            result = send_to_whatsapp(reply_data)
            print(f"\nResultado del envío: {result}\n")
        except Exception as e:
            print(f"\nError al enviar mensaje: {e}\n")
            continue


def text_message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data


def recordatorio_template(number, turno_data):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "template",
            "template": {
                "name": "reserva_recordatorio",
                "language": {"code": "es_AR"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "parameter_name": "nombre", "text": turno_data["nombre_usuario"]}, 
                            {"type": "text", "parameter_name": "servicio", "text": turno_data["servicio"]},
                            {"type": "text", "parameter_name": "hora_turno", "text": turno_data["hora"]},  
                            {"type": "text", "parameter_name": "nombre_empleado", "text": turno_data["nombre_empleado"]}
                    ]
                    }
                ]
            }
        }
    )
    return data


def send_to_whatsapp(data):
    try:
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + ACCESS_TOKEN}
        print("se envia ", data)
        response = requests.post(WHATSAPP_URL, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.text #.status_code
    except Exception as e:
        return e,403


# Funciones de ejemplo (debes adaptarlas a tu lógica)
def obtener_turnos_para_dia(fecha: datetime.date):
    """
    Simula la obtención de turnos para una fecha determinada.
    Reemplaza esta función con la lógica que consulte tu base de datos.
    """

    url = f"{BASE_URL}/turnos/agendados/{fecha}"
    turnos = requests.get(url)

    return turnos.json()