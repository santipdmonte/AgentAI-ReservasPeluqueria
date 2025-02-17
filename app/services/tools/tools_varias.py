from langchain_core.tools import tool
from app.config import BASE_URL
import requests
from typing_extensions import Annotated
from langgraph.prebuilt import InjectedState
from typing import Optional
from pydantic import Field
from langchain_core.tools import tool


@tool
def encontrar_horarios_disponibles(
    date: str = Field(description = "Fecha en la cual buscaremos horarios disponibles string en formato YYYY-MM-DD"),
    hairdresser_id: Optional[str] = Field(description = "ID del Peluquero con el que realizas la reserva")
):
    """Encontrar horarios disponibles por fecha y peluquero (Opcional)"""

    try:


        data = {
            "fecha": date,
            "empleado_id": hairdresser_id
        }

        url = f"{BASE_URL}/turnos/disponibles"

        response = requests.get(url, params=data)

        if response.status_code == 200:
            print("Horarios disponibles: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al buscar horarios disponibles: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al buscar horarios disponibles: ", e)
        return None
    

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
    