from langchain_core.tools import tool
from app.config import BASE_URL
import requests
from typing_extensions import Annotated
from langgraph.prebuilt import InjectedState
from typing import Optional
from pydantic import Field
from langchain_core.tools import tool

    
@tool
def obtener_informacion_peluqueros():
    """Obtener toda la informacion sobre los peluqueros disponibles"""

    try:

        url = f"{BASE_URL}/empleados"

        response = requests.get(url)

        if response.status_code == 200:
            print("Peluqueros disponibles: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al obtener los peluqueros: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener los peluqueros: ", e)
        return None
    

@tool
def crear_peluquero(
    nombre: str = Field(..., title="Nombre del Peluquero"),
    especialidad: int = Field(..., title="ID de la Especialidad"),
):
    """Crear un nuevo peluquero"""

    try:

        url = f"{BASE_URL}/empleados"
        data = {
            "nombre": nombre,
            "especialidad": especialidad
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print("Peluquero creado: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al crear el peluquero: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al crear el peluquero: ", e)
        return ("Error en la solicitud al crear el peluquero: ", e)
    

@tool
def eliminar_peluquero(
    id_peluquero: int = Field(..., title="ID del Peluquero"),
):
    """Eliminar un peluquero"""

    try:

        url = f"{BASE_URL}/empleados/{id_peluquero}"

        response = requests.delete(url)

        if response.status_code == 200:
            print("Peluquero eliminado: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al eliminar el peluquero: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al eliminar el peluquero: ", e)
        return ("Error en la solicitud al eliminar el peluquero: ", e)
    

@tool   
def editar_peluquero(
    id_pelquero: int = Field(..., title="ID del Peluquero a editar"),
    nombre: Optional[str] = Field(None, title="Nombre del Peluquero"),
    especialidad: Optional[int] = Field(None, title="ID de la Especialidad"),
):
    try:
        
        url = f"{BASE_URL}/servicios/{id_pelquero}" 

        payload = {}
        if nombre:
            payload["nombre"] = nombre
        
        if especialidad:
            payload["especialidad"] = especialidad

        if not payload:
            print("\n\nNo se ha especificado ningun campo para editar")
            return ("No se ha especificado ningun campo para editar")

        response = requests.put(url, json=payload)

        if response.status_code == 200:
            print("Peluquero editado: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al editar el peluquero: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al editar el peluquero: ", e)
        return ("Error en la solicitud al editar el peluquero: ", e)        
    