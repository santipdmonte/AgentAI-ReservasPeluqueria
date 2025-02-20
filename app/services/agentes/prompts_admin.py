from app.utils.helpers import fecha_hora_actual, nombre_dia
from app.services.schemas import State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import trim_messages

from app.config import BASE_URL
import requests



def get_formatted_messages(state: State, model):

    # Get empleados data
    try:
        url = f"{BASE_URL}/empleados"
        empleados_info_json= requests.get(url).json()

        empleados_info = ""
        for empleado in empleados_info_json:
            empleados_info += f"{empleado['nombre']} - Especialidad ID: {empleado['especialidad']} (ID Empleado: {empleado['id']}) \n"

    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener los empleados: ", e)
        empleados_info = ""

    # Get servicios data
    try:
        servicios_info_json = requests.get(f"{BASE_URL}/servicios").json()

        servicios_info = ""
        for servicio in servicios_info_json:
            servicios_info += f"{servicio['nombre']} - Precio: ${servicio['precio']} (ID Servicio: {servicio['id']}) -  \n"
    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener los servicios: ", e)
        servicios_info = ""

    

    prompt = f"""
Para las fechas tene en cuenta que hoy es {nombre_dia} y la fecha y hora es: {fecha_hora_actual}"
Eres el administrador de una peluqueria el cual tiene acceso a operaciones sensibles 
El mensaje se enviara por whatsapp, adaptar el formato de respuesta para ese medio
NO le muestres los ID a los usuario en la conversacion, solo usalos para la herramienta

Esta es informacion sobre los empleados y los servicios disponibles

=== Informacion Empleados ===
{empleados_info}

=== Informacion Servicios ===
{servicios_info}
"""

    prompt_template = ChatPromptTemplate.from_messages([( "system", prompt), ('placeholder', '{messages}')]) 

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


