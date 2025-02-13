from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services import wpp_tools
import datetime

from app.config import BASE_URL
import requests


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
        print("\n ============================ \n") 

        response_list = []
        reply_data = wpp_tools.text_message(telefono,mensaje)
        response_list.append(reply_data)

        # wpp_tools.enviar_mensaje_whatsapp(reply_data)

         # Enviar mensajes
        for item in response_list:
            result = wpp_tools.enviar_mensaje_whatsapp(item)
            print(f"\nResultado del envío: {result}\n")

    print(f"Recordatorios enviados para los turnos del {dia_siguiente}\n")


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



# # Inicializa el scheduler
# scheduler = BackgroundScheduler()
# scheduler.add_job(enviar_recordatorio, CronTrigger(hour=18, minute=0))
# # scheduler.start() -> Inizializado en el main.py



enviar_recordatorio()