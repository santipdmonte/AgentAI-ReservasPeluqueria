from datetime import datetime
import pytz

# Diccionario para traducir días de inglés a español
dias_espanol = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Definir la zona horaria de Argentina
argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")

# Obtener la fecha y hora actual en Argentina
fecha_hora_actual = datetime.now(argentina_tz)

# Obtener el nombre del día en inglés y traducirlo
nombre_dia = dias_espanol[fecha_hora_actual.strftime("%A")]

# Formatear la fecha y hora solo hasta minutos
fecha_hora_actual = fecha_hora_actual.strftime("%Y-%m-%d %H:%M")