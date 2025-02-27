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
    

@tool
def crear_horarios_recurrentes_empelados(
    dia: str,
    hora_inicio: str,
    hora_fin: str,
    empleado_id: Optional[str] = None
    ):
    """
    Crear horarios recurrentes para un empleado:
    dia: El dia de la semana (L M X J V S D) a crear el horario recurrente
    hora_inicio: La hora de inicio del horario recurrente
    hora_fin: La hora de fin del horario recurrente
    empleado_id: Id del peluquero

    (Un empleado puede tener varios horarios recurrentes en un mismo dia)
    """
    try:

        intervalo = 30

        # Validar que la hora de inicio sea menor a la hora de fin
        if hora_inicio >= hora_fin:
            error = "La hora de inicio debe ser menor a la hora de fin"
            print(f"\n\n{error}")
            return (f"Error: {error}")
        
        # Validar que el dia sea válido
        if dia not in ["L", "M", "X", "J", "V", "S", "D"]:
            error = "El día debe ser uno de los siguientes: L, M, X, J, V, S, D"
            print(f"\n\n{error}")
            return (f"Error: {error}")

        data = {
            "dia": dia,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "intervalo": intervalo,
            "empleado_id": empleado_id
        }

        url = f"{BASE_URL}/horarios"

        response = requests.post(url, params=data)

        if response.status_code == 200:
            print("Horario recurrente creado: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al crear el horario recurrente: ", response.status_code, response.json())
            return ("Error al crear el horario recurrente:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al crear el horario recurrente: ", e)
        return ("Error en la solicitud al crear el horario recurrente: ", e)


@tool
def ver_horarios_recurrentes(
    dia: Optional[str] = None, 
    hairdresser_id: Optional[str] = None
    ):
    """
    Ver horarios recurrentes

    Filtros Opcionales:
        - dia: Un dia de la semana (L M X J V S D)
        - hairdresser_id: Id del peluquero
    """
    try:

        params = {}
        
        # Validar y agregar dia si existe
        if dia is not None:
            if dia not in ["L", "M", "X", "J", "V", "S", "D"]:
                error = "El día debe ser uno de los siguientes: L, M, X, J, V, S, D"
                print(f"\n\n{error}")
                return f"Error: {error}"
            params["dia"] = dia
            
        # Agregar hairdresser_id si existe
        if hairdresser_id is not None:
            params["empleado_id"] = hairdresser_id
        
        url = f"{BASE_URL}/horarios"
        response = requests.get(url, params=params)

        if response.status_code == 200:
            print("Horarios recurrentes: ", response.json())
            return response.json()
        
        print("\n\nError al ver los horarios recurrentes: ", response.status_code, response.json())
        return ("Error al ver los horarios recurrentes:", response.status_code, response.json())
    
    except requests.RequestException as e:
        print("\n\nError en la solicitud al ver los horario recurrente: ", e)
        return ("Error en la solicitud al ver los horario recurrente: ", e)
    

@tool
def eliminar_horarios_recurrentes(id: str):
    """ Eliminar horarios recurrentes por id """
    try:

        url = f"{BASE_URL}/horarios/{id}"

        response = requests.delete(url)

        if response.status_code == 200:
            print("Horario recurrente eliminado: ", response.json())
            return response.json()
        
        print("\n\nError al horario recurrente: ", response.status_code, response.json())
        return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al horario recurrente: ", e)
        return ("Error en la solicitud al horario recurrente: ", e)


@tool
def bloquear_horarios(
    date: str,
    hora_inicio: str,
    hora_fin: str,
    hairdresser_id: Optional[str] = None
    ):
    """
    Bloquea el horario de un peluquero en una fecha especifica:
    date: Fecha a bloquear
    hora_inicio: Hora de inicio del bloqueo
    hora_fin: Hora de fin del bloqueo
    hairdresser_id: Id del peluquero

    (Esta herramienta se utiliza para bloquear horarios de un peluquero en una fecha especifica por algun motivo especifico no recurrente)
    """
    pass


