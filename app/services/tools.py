from langchain_core.tools import tool
from app.services.schemas import Reservation, State, FindFreeSpaces, UserInfo
from app.config import BASE_URL
import requests


@tool
def crear_reserva(reservation_info: Reservation):
    """Confirma y crea la reserva"""

    try:

        turno_data = {
            "usuario_id": reservation_info.user_id,                     # UUID
            "empleado_id": "40291357-7f35-4968-a4fd-9e451a0dad0e",      #reservation_info.empleado_id,     # UUID
            "servicio_id": "ea685bf6-eb64-4f01-9239-3ef42402c112",      #reservation_info.servicio_id,     # UUID
            "fecha": reservation_info.date,                             # 'YYYY-MM-DD'
            "hora": reservation_info.time                               # 'HH:MM:SS'
            }

        response = requests.post(
            f"{BASE_URL}/turnos/", 
            json=turno_data)

        if response.status_code == 200:
            print (f"\n\nTurno creado correctamente: {response.json()}")
            return (f"Turno creado correctamente: {response.json()}")
        
        else:
            print (f"\n\nError al crear el turno: {response.status_code} {response.json()}")
            return (f"Error al crear el turno: {response.status_code} {response.json()}")

    except requests.RequestException as e:
        print (f"\n\nError en la solicitud al crear el turno: {e}")
        return (f"Error en la solicitudal crear el turno: {e}")
    



@tool
def crear_usuario(user_info: UserInfo):
    """Crea el usuario"""

    telefono = "3413918906"

    try:

        user_info = {
                "nombre": user_info.nombre,          
                "telefono": telefono,     
                "email": user_info.email,   
            }

        response = requests.post(
            f"{BASE_URL}/usuarios/", 
            json=user_info)

        if response.status_code == 200:
            user_data = response.json()
            print (f"\n\nUruario creado correctamente: {user_data}")
            return (f"Uruario creado correctamente: {user_data}")
        
        else:
            print(f"\n\nError al crear el usuario: {response.status_code} {response.json()}")
            return (f"Error al crear el usuario: {response.status_code} {response.json()}")

    except requests.RequestException as e:
        print (f"\n\nError en la solicitud al crear el usuario: {e}")
        return (f"Error en la solicitud al crear el usuario: {e}")



@tool
def obtener_reservas_del_cliente(user_id: str):
    """Obtenes todas las reservas de un cliente"""

    try:

        url = f"{BASE_URL}/turnos/user/{user_id}"
        response = requests.get(url)

        if response.status_code == 200:
            user_data = response.json()
            print("\n\nReservas encontradas: ", user_data)
            return user_data
        
        else:
            print("\n\nError al obtener las reservas del cliente:", response.status_code, response.json())
            return ("Error al obtener las reservas del cliente:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener las reservas del cliente:", e)
        return None



@tool
def modificar_reserva(reservation_id: str, reservation_info: Reservation):
    """Modifcar reserva"""

    try:

        nuevo_turno_data = {
                "usuario_id": reservation_info.user_id,                 # UUID -> Se podria obtener del reservation_id
                "empleado_id": "4f79dc51-2a24-4831-b0a9-919b961e30ef",  # reservation_info.empleado_id,     # UUID
                "servicio_id": "ea685bf6-eb64-4f01-9239-3ef42402c112",  # reservation_info.servicio_id,     # UUID
                "fecha": reservation_info.date,                         # 'YYYY-MM-DD'
                "hora": reservation_info.time                           # 'HH:MM:SS'
            }

        url = f"{BASE_URL}/edit/{reservation_id}"
        response = requests.put(url, json=nuevo_turno_data)


        if response.status_code == 200:
            print (f"\n\nTurno modificado correctamente: {response.json()}")
            return (f"Turno modificado correctamente: {response.json()}")
        
        else:
            print (f"\n\nError al modificar el turno: {response.status_code} {response.json()}")
            return (f"Error al modificar el turno: {response.status_code} {response.json()}")

    except requests.RequestException as e:
        print (f"\n\nError en la solicitud al modificar el turno: {e}")
        return (f"Error en la solicitud al modificar el turno: {e}")



@tool
def cancelar_reserva(reservation_id: str):
    """cancelar reserva"""

    try:

        url = f"{BASE_URL}/turnos/{reservation_id}"

        response = requests.put(url)

        if response.status_code == 200:
            response_json = response.json()
            print("\n\nReserva cancelada con exito!")
            return "Reserva cancelada con exito!"
        
        else:
            print("\n\nError al cancelar la reserva: ", response.status_code, response.json())
            return ("Error al cancelar la reserva: ", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al cancelar la reserva: ", e)
        return None



@tool
def encontrar_horarios_disponibles(query: FindFreeSpaces):
    """Encontrar horarios disponibles"""

    try:

        url = f"{BASE_URL}/turnos/disponibles/{query.date}"

        response = requests.get(url)

        if response.status_code == 200:
            print("Horarios disponibles: ", response.json())
            return response.json()
        
        else:
            print("\n\nError al buscar horarios disponibles: ", response.status_code, response.json())
            return ("Error:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al buscar horarios disponibles: ", e)
        return None