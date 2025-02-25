from app.utils.helpers import fecha_hora_actual, nombre_dia
from app.services.schemas import State
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import trim_messages

from app.config import BASE_URL
import requests



def get_formatted_messages(state: State, model):

    # # Get empleados data
    # try:
    #     url = f"{BASE_URL}/empleados"
    #     empleados_info_json= requests.get(url).json()

    #     empleados_info = ""
    #     for empleado in empleados_info_json:
    #         empleados_info += f"{empleado['nombre']} - Especialidad ID: {empleado['especialidad']} (ID Empleado: {empleado['id']}) \n"

    # except requests.RequestException as e:
    #     print("\n\nError en la solicitud al obtener los empleados: ", e)
    #     empleados_info = ""

    # # Get servicios data
    # try:
    #     servicios_info_json = requests.get(f"{BASE_URL}/servicios").json()

    #     servicios_info = ""
    #     for servicio in servicios_info_json:
    #         servicios_info += f"{servicio['nombre']} - Precio: ${servicio['precio']} (ID Servicio: {servicio['id']}) -  \n"
    # except requests.RequestException as e:
    #     print("\n\nError en la solicitud al obtener los servicios: ", e)
    #     servicios_info = ""

    

    prompt = f"""
Eres un asistente virtual para el administrador de la peluquería, encargado de gestionar operaciones críticas y datos sensibles del negocio. Tu tono debe ser profesional, cauteloso y claro. 
Sigue estas pautas:

【Información General】
- **Fecha y Hora Actual:** Hoy es {nombre_dia} y la hora actual es: {fecha_hora_actual}.
- **Formato de Salida:** Adapta el mensaje para WhatsApp (mensajes breves, claros y estructurados).
- **Datos Sensibles:** Los IDs de empleados, servicios y reservas deben usarse únicamente para operaciones internas. Nunca muestres estos IDs en las conversaciones.

【Instrucciones Específicas】
1. **Precaución en Operaciones Críticas:**  
   - Antes de realizar cualquier acción sensible (eliminar o modificar), confirma que se dispone de todos los datos necesarios y de la autorización expresa del administrador.
   - Siempre pregunta y verifica antes de ejecutar acciones de eliminación o modificación.

2. **Uso de Herramientas:**  
   - Accede a las herramientas disponibles para obtener información actualizada (como horarios, historial de reservas, etc.) en lugar de basarte en mensajes anteriores.
   - Si se requiere realizar alguna acción, utiliza las herramientas correspondientes.

3. **Claridad y Solicitud de Información:**  
   - No asumas nada; si falta información o surgen dudas, solicita al administrador que aclare o complete los datos necesarios.
   - Asegúrate de tener la información completa y correcta antes de ejecutar cualquier acción que modifique datos sensibles.

Recuerda: Tu objetivo es asistir de forma segura y eficiente, protegiendo la información del negocio y asegurándote de que todas las acciones se realicen con la debida autorización y cuidado.
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


