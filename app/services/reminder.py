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
    turnos_por_usuario = agrupar_turnos_por_usuario(turnos)

    print("\n ============================ \n")
    print(turnos_por_usuario)
    print("\n ============================ \n")

    for user_data in turnos_por_usuario:
        nombre = user_data['nombre_usuario']
        telefono = user_data['telefono']

        if len(user_data['turnos']) == 1:

            turno = user_data['turnos'][0]
            mensaje = f"Hola {nombre}, recorda que mañana tenes turno a las *{turno['hora']}* con *{turno['nombre_empleado']}*. \n¡Nos vemos! 🎉"

        else: 

            turnos = user_data['turnos']

            mensaje = f"Hola {nombre}, recorda que mañana tenes los siguientes turnos:\n\n"

            for turno in turnos:
                mensaje += f"- *{turno['hora']}* {turno['servicio']} con *{turno['nombre_empleado']}*\n"

            mensaje += "\n¡Nos vemos! 🎉"
 
        print(mensaje) 
         
        try:
            reply_data = text_message(telefono,mensaje)
            # result = send_to_whatsapp(reply_data)
            # print(f"\nResultado del envío: {result}\n")
            print (f"\n{reply_data} \n")
        except Exception as e:
            print(f"\nError al enviar mensaje: {e}\n")
            continue

        print("\n ============================ \n")

    print(f"Recordatorios enviados para los turnos del {dia_siguiente}\n")


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
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    

def send_location(number, latitude, longitude, location_name, adress):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "location",
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "name": location_name,
                "address": adress
            }
        }
    )
    return data


def agrupar_turnos_por_usuario(turnos):
    """
    Agrupa los turnos obtenidos por usuario basándose en 'usuario_id'.
    Retorna un diccionario donde la clave es el usuario_id y el valor es un
    diccionario con la información del usuario y una lista de sus turnos.
    """
    # TODO: Ajustar logica
    turnos_por_usuario = {}
    for turno in turnos:
        usuario_id = turno['usuario_id']
        if usuario_id not in turnos_por_usuario:
            turnos_por_usuario[usuario_id] = {
                'nombre_usuario': turno['nombre_usuario'],
                'telefono': turno['telefono'],
                'turnos': []
            }
        turnos_por_usuario[usuario_id]['turnos'].append({
            'hora': turno['hora'][:5],
            'servicio': turno['servicio'],
            'nombre_empleado': turno['nombre_empleado']
        })
    return list(turnos_por_usuario.values())


# Funciones de ejemplo (debes adaptarlas a tu lógica)
def obtener_turnos_para_dia(fecha: datetime.date):
    """
    Simula la obtención de turnos para una fecha determinada.
    Reemplaza esta función con la lógica que consulte tu base de datos.
    """

    url = f"{BASE_URL}/turnos/agendados/{fecha}"
    turnos = requests.get(url)

    return turnos.json()

# Ejecutar la función de envío de recordatorio
# enviar_recordatorio()

# reply_data = text_message('543413918950',"Mensaje de prueba")
# result = send_to_whatsapp(reply_data)
# print(result)