#!/usr/bin/env python3
import os
import uuid
from datetime import datetime, timedelta
from app.config import GOOGLE_TOKEN
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define el alcance necesario para gestionar el calendario
SCOPES = ['https://www.googleapis.com/auth/calendar']

def crear_evento(fecha_hora_inicio, fecha_hora_fin):
    """Crea un evento en el calendario de Google Calendar."""

    service = obtener_servicio()

    evento_inicio = formatear_fecha(fecha_hora_inicio)
    evento_fin = formatear_fecha(fecha_hora_fin)
    
    evento = {
        'summary': 'Reserva de cita',
        'location': 'Ubicación del evento',
        'description': 'Detalle de la reserva en la aplicación',
        'start': {
            'dateTime': evento_inicio,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': evento_fin,
            'timeZone': 'America/Los_Angeles',
        },
    }
    
    # Inserta el evento en el calendario "primary"
    evento_creado = service.events().insert(
        calendarId='primary',
        body=evento,
        conferenceDataVersion=1
    ).execute()
    
    print('Evento creado correctamente.')
    print('Link del evento en Google Calendar: {}'.format(evento_creado.get('htmlLink')))
    
    # Si se generó la reunión, se muestra el link para unirse
    if 'hangoutLink' in evento_creado:
        print('Link para unirse a la reunión (Google Meet): {}'.format(evento_creado.get('hangoutLink')))
    else:
        print('No se generó un link de Google Meet para este evento.')


def formatear_fecha(fecha_hora):
    """Convierte la fecha de 'YYYY/MM/DD hh:mm' a formato ISO 8601 para Google Calendar."""
    dt = datetime.strptime(fecha_hora, "%Y/%m/%d %H:%M")
    return dt.isoformat()  # Devuelve la fecha en formato ISO

def obtener_servicio():
    """Autentica al usuario y devuelve el servicio de Calendar API."""
    creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN, SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service


def main():
    service = obtener_servicio()
    crear_evento(service)

if __name__ == '__main__':
    main()
