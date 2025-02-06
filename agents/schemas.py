from pydantic import BaseModel, Field
from uuid import UUID
from typing import Literal, Annotated, Optional
from typing_extensions import TypedDict
from enum import Enum
from langgraph.graph.message import AnyMessage, add_messages

class State(TypedDict):
    user_id: str
    name: str
    phone_number: str
    messages: Annotated[list, add_messages]

class Hairdresser(str, Enum): # TODO: Get from database all the hairdressers
    CARLOS = "Carlos" # "40291357-7f35-4968-a4fd-9e451a0dad0e"
    PEDRO = "Pedro" # "7e5d454c-9aad-4c82-8476-8fc6e6d570cd"
    JUANA = "Juana" # "aa0cc7cc-fc6e-4530-9a83-a3b4850959cc"

class Services(str, Enum): # TODO: Get from database all the services
    CORTE_CABELLO = "Corte de cabello" # "ea685bf6-eb64-4f01-9239-3ef42402c112"

class Reservation(BaseModel):
    user_id: str = Field(description = "ID del usuario que realiza la reserva")
    name: str = Field(description = "Nombre de la persona que hace la reserva")
    date: str = Field(description = "Fecha de la reserva")
    time: str = Field(description = "Hora de la reserva")
    # hairdresser: Hairdresser = Field(description = "Peluquero con el que realizas la reserva")
    # observation: Optional[str] = Field(default=None, description = "Observacion opcional sobre la reserva")

class UserInfo(BaseModel):
    nombre: str = Field(description = "Nombre del usuario")
    email: Optional[str] = Field(description = "Email del usuario")

class FindFreeSpaces(BaseModel):
    date: str = Field(description = "Fecha en la cual buscaremos horarios disponibles")
    # hairdresser: Optional[Hairdresser] = Field(description = "Peluquero con el que desea buscar turnos libres. Este campo es opciona, si no se especifica un peluquero no hace falta para la consulta de la herramienta")