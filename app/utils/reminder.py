import datetime
import json
import requests
from app.config import BASE_URL
from app.utils.wpp_tools import send_to_whatsapp


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
                            {"type": "text", "parameter_name": "hora_turno", "text": turno_data["hora"][:5]},  
                            {"type": "text", "parameter_name": "nombre_empleado", "text": turno_data["nombre_empleado"]}
                    ]
                    }
                ]
            }
        }
    )
    return data


def obtener_turnos_para_dia(fecha: datetime.date):
    """
    Simula la obtención de turnos para una fecha determinada.
    Reemplaza esta función con la lógica que consulte tu base de datos.
    """

    url = f"{BASE_URL}/turnos/agendados/{fecha}"
    turnos = requests.get(url)

    return turnos.json()