from langchain_core.tools import tool
from app.config import BASE_URL
import requests
from typing_extensions import Annotated
from langgraph.prebuilt import InjectedState
from typing import Optional
from langgraph.types import Command
from langchain_core.tools import InjectedToolCallId, tool
from langchain_core.messages import ToolMessage


@tool
def crear_usuario(nombre: str, phone_number: Annotated[Optional[str], InjectedState("phone_number")], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Crea el usuario"""

    if not phone_number:
        print("\n\nEl numero de telefono no se cargo correctamente, volver a intentar")
        return ("El numero de telefono no se cargo correctamente, volver a intentar")

    try:

        user_info = {
                "nombre": (nombre).capitalize(),          
                "telefono": phone_number     
            }

        response = requests.post(
            f"{BASE_URL}/usuarios/", 
            json=user_info)

        if response.status_code == 200:
            user_data = response.json()
            response = f"Usuario creado correctamente: {user_data}"
            print (f"\n\n {response}")

            state_update = {
                "user_id": str(user_data["id"]),
                "name": user_data["nombre"],
                "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
            }
            return Command(update=state_update)
        
        else:
            print(f"\n\nError al crear el usuario: {response.status_code} {response.json()}")
            return (f"Error al crear el usuario: {response.status_code} {response.json()}")

    except requests.RequestException as e:
        print (f"\n\nError en la solicitud al crear el usuario: {e}")
        return (f"Error en la solicitud al crear el usuario: {e}")
    

@tool
def modificar_nombre_usuario(nombre: str, user_id: Annotated[Optional[str], InjectedState("user_id")], tool_call_id: Annotated[str, InjectedToolCallId]):
    """Modifcar usuario: Modificar el nombre del usuario"""

    if not user_id:
        print("\n\nParece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")
        return ("Parece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")

    try:

        payload = {
            "id": user_id,
            "nombre": (nombre).capitalize()
        }   
   

        response = requests.put(
            f"{BASE_URL}/usuarios/", 
            json=payload
        )

        if response.status_code == 200:
            user_data = response.json()
            print (f"\n\nUsuario modificado correctamente: {user_data}")
            response =  (f"Usuario modificado correctamente: {user_data}")
            state_update = {
                "name": user_data["nombre"],
                "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
            }
            return Command(update=state_update)
        
        else:
            print (f"\n\nError al modificar el usuario: {response.status_code} {response.json()}")
            return (f"Error al modificar el usuario: {response.status_code} {response.json()}")

    except requests.RequestException as e:
        print (f"\n\nError en la solicitud al modificar el usuario: {e}")
        return (f"Error en la solicitud al modificar el usuario: {e}")
    
@tool
def historial_usuario(user_id: Annotated[Optional[str], InjectedState("user_id")]):
    """Historial de turnos pasados del usuario. Para saber con que peluquero se atendio y que servicios se realizo anteriormente"""

    try:

        url = f"{BASE_URL}/usuarios/historial/{user_id}"

        response = requests.get(url)

        if response.status_code == 200:
            print("Ultimos 6 turnos cliente: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al obtener los ultimos turnos del cliente: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud de historial del cliente: ", e)
        return None