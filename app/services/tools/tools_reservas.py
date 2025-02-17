from langchain_core.tools import tool
from app.services.schemas import Reservation, FindFreeSpaces, UserInfo
from app.config import BASE_URL
import requests
from typing_extensions import Annotated
from langgraph.prebuilt import InjectedState
from typing import Optional
from langchain_core.tools import tool


@tool
def crear_reserva(reservation_info: Reservation, user_id: Annotated[Optional[str], InjectedState("user_id")]):
    """Confirma y crea la reserva"""

    if not user_id:
        print("\n\nParece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")
        return ("Parece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")

    try:

        turno_data = {
            "usuario_id": user_id,                                      
            "empleado_id": reservation_info.hairdresser_id,             # UUID
            "servicio_id": reservation_info.service_id,                 # UUID
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
def obtener_reservas_del_cliente(user_id: Annotated[Optional[str], InjectedState("user_id")]):
    """Obtener todas las reservas de un cliente"""

    if not user_id:
        print("\n\nParece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")
        return ("Parece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")

    try:

        url = f"{BASE_URL}/turnos/user/{user_id}"
        response = requests.get(url)

        if response.status_code == 200:
            reservations_data = response.json()
            print("\n\nReservas encontradas: ", reservations_data)
            return reservations_data
        
        else:
            print("\n\nError al obtener las reservas del cliente:", response.status_code, response.json())
            return ("Error al obtener las reservas del cliente:", response.status_code, response.json())
        
    except requests.RequestException as e:
        print("\n\nError en la solicitud al obtener las reservas del cliente:", e)
        return None
    

@tool
def modificar_reserva(reservation_id: str, reservation_info: Reservation, user_id: Annotated[Optional[str], InjectedState("user_id")]):
    """Modifcar reserva: Busca disponibilidad del nuevo horario, crea la nueva reserva y cancela el reserva anterior"""

    if not user_id:
        print("\n\nParece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")
        return ("Parece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")

    try:
        
        nuevo_turno_data = {
            "usuario_id": user_id,                                      
            "empleado_id": reservation_info.hairdresser_id,             # UUID
            "servicio_id": reservation_info.service_id,                 # UUID
            "fecha": reservation_info.date,                             # 'YYYY-MM-DD'
            "hora": reservation_info.time                               # 'HH:MM:SS'
            }

        url = f"{BASE_URL}/turnos/edit/{reservation_id}"
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
def cancelar_reserva(reservation_id: str, user_id: Annotated[Optional[str], InjectedState("user_id")]):
    """Cancela la reserva"""

    if not user_id:
        print("\n\nParece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")
        return ("Parece que hubo un error al cargar el id del usuario, volver a intentar mas tarde")

    try:

        # TODO
        # # Validar que el usuario sea el dueño de la reserva
        # reservas = obtener_reservas_del_cliente(user_id)
        # if reservation_id not in reservas["id"]:
        #     print("\n\nEl usuario no tiene una reserva con el id: ", reservation_id)
        #     return ("El usuario no tiene una reserva con el id: ", reservation_id)


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