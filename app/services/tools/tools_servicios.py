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
    """Obtener toda la informacion sobre los servicios disponibles"""

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
    """Crear un nuevo servicio"""

    try:

        url = f"{BASE_URL}/servicios"
        data = {
            "nombre": nombre,
            "precio": precio,
            "duracion": duracion
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
    nombre: Optional[str] = Field(None, title="Nombre del Servicio"),
    precio: Optional[float] = Field(None, title="Precio del Servicio"),
    duracion: Optional[int] = Field(None, title="Duracion del Servicio"),  
    servicio_id: int = Field(..., title="ID del Servicio a editar")
):
    """Editar un servicio"""

    try:

        url = f"{BASE_URL}/servicios/{servicio_id}" 

        payload = {}
        if nombre:
            payload["nombre"] = nombre

        if precio:
            payload["precio"] = precio
        
        if duracion:
            payload["duracion"] = duracion

        if not payload:
            print("\n\nNo se ha especificado ningun campo para editar")
            return ("No se ha especificado ningun campo para editar")

        response = requests.put(url, json=payload)

        if response.status_code == 200:
            print("Servicio editado: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al editar el servicio: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al editar el servicio: ", e)
        return ("Error en la solicitud al editar el servicio: ", e)
    

@tool
def eliminar_servicio(
    servicio_id: str = Field(..., title="ID del Servicio a eliminar")
):
    """Eliminar un servicio"""

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

    