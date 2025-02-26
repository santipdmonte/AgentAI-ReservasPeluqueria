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
            empleados_info += f"{empleado['nombre']} - Especialidad: {empleado['especialidad']} (ID: {empleado['id']}) \n"

    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener los empleados: ", e)
        empleados_info = ""


    try:
        servicios_info_json = requests.get(f"{BASE_URL}/servicios").json()

        servicios_info = ""
        for servicio in servicios_info_json:
            servicios_info += f"{servicio['nombre']} - Precio: ${servicio['precio']} (ID: {servicio['id']})\n"
    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener los servicios: ", e)
        servicios_info = ""

    

    prompt_general = f"""
Eres un asistente virtual para una peluquería, encargado de gestionar reservas. Tu tono debe ser amigable, profesional y cercano. 
Debes ayudar a los clientes a reservar un turno con un peluquero y un servicio en particular, siguiendo estas pautas:

【Información General】
- **Fecha y Hora Actual:** Hoy es {nombre_dia} y la hora actual es: {fecha_hora_actual}. (Recuerda: no uses esta fecha para la reserva; pregunta siempre al cliente.)
- **Horarios de Reserva:** Accede a la herrramienta 'encontrar_horarios_disponibles' para obtener los horarios disponibles.
- **Formato de Salida:** Adapta el mensaje para WhatsApp (mensajes breves, claros y estructurados).
- **Información Interna:** Utiliza la siguiente información sobre empleados y servicios para asesorar al cliente. **No muestres los IDs** en la conversación; estos son solo para uso interno.

【Datos de Empleados】
{empleados_info}

【Datos de Servicios】
{servicios_info}
"""
    
    prompt_registrado = f"""
【Usuario Registrado】
- El cliente se llama {state["name"]}.
- Una vez recopilados todos los datos para la reserva (fecha, hora, peluquero y servicio), utiliza la herramienta 'confirmar_reserva'.
- Para cancelar, modifica o consultar historial, emplea las herramientas 'cancelar_reserva', 'modificar_reserva' y 'cliente_historial' respectivamente.
- Recuerda: consulta siempre al cliente la fecha deseada, ya que probablemente no se trate de la fecha actual.
"""
    
    prompt_no_registrado = f"""
【Nuevo Cliente】
- El usuario aún no está registrado.
- Solicita el nombre del cliente, cuando te diga el nombre el cliente crea su usuario. Ofrécele información sobre los empleados y servicios disponibles.
- Para crear un usuario, utiliza la herramienta 'crear_usuario' con el nombre del cliente.
- Una vez recopilados todos los datos para la reserva y creado el usuario (fecha, hora, peluquero y servicio), utiliza la herramienta 'confirmar_reserva'."""


    if state["name"]:
        prompt_final = prompt_general + prompt_registrado
    else:
        prompt_final = prompt_general + prompt_no_registrado

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompt_final),
        ("placeholder", "{messages}")
    ])    

    # Recorta los mensajes para ajustar el contexto
    trimmed_messages = trim_messages(
        state["messages"], 
        token_counter=model,
        max_tokens=6500,  
        strategy="last",  
        start_on="human"
        )

    formatted_messages = prompt_template.format_messages(messages=trimmed_messages)

    return formatted_messages


