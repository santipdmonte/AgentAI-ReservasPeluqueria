from langchain_core.tools import tool
from app.config import BASE_URL
import requests
from typing_extensions import Annotated
from langgraph.prebuilt import InjectedState
from typing import Optional
from pydantic import Field
from langchain_core.tools import tool
    

@tool
def obtener_informacion_servicios():
    """Obtener informacion sobre los servicios disponibles"""

    try:

        url = f"{BASE_URL}/servicios"

        response = requests.get(url)

        if response.status_code == 200:
            print("Servicios disponibles: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al obtener los servicios: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener los servicios: ", e)
        return None
    

@tool
def crear_servicios(
    nombre: str = Field(..., title="Nombre del Servicio"),
    precio: float = Field(..., title="Precio del Servicio"),
    duracion: int = Field(..., title="Duracion del Servicio"),
):
    """
    Crear un nuevo servicio:
    
    Esta herramienta crear un nuevo servicio con los siguientes campos:
    
    - Nombre del Servicio
    - Precio del Servicio
    - Duracion del Servicio    
    """

    try:

        url = f"{BASE_URL}/servicios"
        data = {
            "nombre": nombre,
            "precio": precio,
            "duracion_minutos": duracion
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("Servicio creado: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al crear el servicio: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al crear el servicio: ", e)
        return ("Error en la solicitud al crear el servicio: ", e)
    

@tool
def editar_servicio(
    servicio_id: str,
    nombre: Optional[str] = None,
    precio: Optional[float] = None,
    duracion: Optional[int] = None
):
    """
    Editar un servicio existente.
    
    Esta herramienta permite modificar uno o más aspectos de un servicio existente:
    - Cambiar el nombre
    - Actualizar el precio
    - Modificar la duración
    
    Requiere el ID del servicio y al menos un campo para modificar.
    """
    try:
        url = f"{BASE_URL}/servicios/{servicio_id}" 

        payload = {}
        if nombre is not None:
            payload["nombre"] = nombre

        if precio is not None:
            payload["precio"] = precio
        
        if duracion is not None:
            payload["duracion_minutos"] = duracion

        if not payload:
            print("\n\nNo se ha especificado ningun campo para editar")
            return "No se ha especificado ningun campo para editar"

        response = requests.put(url, json=payload)

        if response.status_code == 200:
            print("Servicio editado: ", response.json())
            return response.json()
        
        else:
            error_message = f"Error al editar el servicio: {response.status_code} - {response.json()}"
            print(f"\n\n{error_message}")
            return error_message
        
    except requests.RequestException as e:
        error_message = f"Error en la solicitud al editar el servicio: {e}"
        print(f"\n\n{error_message}")
        return error_message

    

@tool
def eliminar_servicio(
    servicio_id: str
):
    """Eliminar un servicio: elimina un servicio existente por su ID"""

    try:

        url = f"{BASE_URL}/servicios/{servicio_id}"

        response = requests.delete(url)

        if response.status_code == 200:
            print("Servicio eliminado: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al eliminar el servicio: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al eliminar el servicio: ", e)
        return ("Error en la solicitud al eliminar el servicio: ", e)

    