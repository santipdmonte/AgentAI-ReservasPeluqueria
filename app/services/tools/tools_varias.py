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
    date: str,
    hairdresser_id: Optional[str] = None
):
    """Encontrar horarios disponibles:
    
    Esta herramienta busca horarios disponibles por fecha, y opcionalmente filtra por el id del peluquero
    
    - Fecha: para encontrar horarios disponibles
    - id del peluquero: para filtrar horarios disponibles por peluquero (Campo opcional)
    """

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
    
    