from app.utils.helpers import fecha_hora_actual, nombre_dia
from app.services.schemas import State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import trim_messages

from app.config import BASE_URL
import requests



def get_formatted_messages(state: State, model):


    try:
        url = f"{BASE_URL}/empleados"
        empleados_info_json= requests.get(url).json()

        empleados_info = ""
        for empleado in empleados_info_json:
            empleados_info += f"{empleado['nombre']} - Especialidad ID: {empleado['especialidad']} (ID Empleado: {empleado['id']}) \n"

    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener los empleados: ", e)
        empleados_info = ""


    try:
        servicios_info_json = requests.get(f"{BASE_URL}/servicios").json()

        servicios_info = ""
        for servicio in servicios_info_json:
            servicios_info += f"{servicio['nombre']} - Precio: ${servicio['precio']} (ID Servicio: {servicio['id']}) -  \n"
    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener los servicios: ", e)
        servicios_info = ""

    

    prompt = f"""
Sos un asistente para una peluqueria encargado de tomar las reservas de los clientes

Para las fechas tene en cuenta que hoy es {nombre_dia} y la fecha y hora es: {fecha_hora_actual}
Esta es la fecha y hora actual, el clientes seguramente quiera realizar una reserva para una fecha proxima, 
por lo que no tomes por defecto la fecha actual para la reserva, sino que preguntale al cliente

Las reservas se toman cada 30 minutos. Comienzan a las 9AM y el ultimo turno es 18:30

El mensaje se enviara por whatsapp, adaptar el formato de respuesta para ese medio

NO le muestres los ID a los usuario en la conversacion, solo usalos para la herramienta

Esta es informacion sobre los empleados y los servicios disponibles:
Utilizala para las herramientas y para ayudar a los clientes a elegir

=== Informacion Empleados ===
{empleados_info}

=== Informacion Servicios ===
{servicios_info}
"""
    
    prompt_usuarios_registrados = f"""
El cliente con el que estas hablando se llama {state["name"]}
Una vez que tengas toda la informacion necesaria para la reserva procede a utilizar la herramienta que confirma la reserva
Tene en cuenta que para realizar una reserva debes saber el ID del peluquero y el ID del servicio, pueden consultarlo en las herramientas correspondientes
Para cancelar una reserva usa la tool 'cancelar_reserva'
Para modificar o editar una reserva usa unicamente la tool 'modificar_reserva' (no hace falta cancelar ni volver a hacer la reserva)
Para saber la disponibilidad de turnos usa la herramienta 'encontrar_horarios_disponibles', puedes filtrar opcionalmente por peluquero
Puedes usar la herramienta de 'cliente_historial' para ver el historial de reservas del cliente y saber con que peluquero se suele atender y que servicio suele tomar
"""
    
    prompt_usuarios_no_registrados = f"""
Este cliente no esta registrado, para realizar una reserva el usuario debe estar creado.
Para crear el usuario necesitas el nombre. Podes crear el usuario accediendo a la herramienta correspondiente
La herramienta ya sabe el numero del cliente, no hace falta que se lo preguntes
"""


    if state["name"]:
        prompt += prompt_usuarios_registrados
    
    else:
        prompt += prompt_usuarios_no_registrados

    prompt_template = ChatPromptTemplate.from_messages([( "system", prompt), ('placeholder', '{messages}')]) 
    # prompt_template = ChatPromptTemplate.from_messages([( "system", ""), ('placeholder', '{messages}')]) 

    # Trim messages to fit within the context window
    trimmed_messages = trim_messages(
        state["messages"], 
        token_counter=model,
        max_tokens=4000,  # Context window
        strategy="last",  # Most recent messages
        start_on="human"
        )

    formatted_messages = prompt_template.format_messages( messages = trimmed_messages )

    return formatted_messages


