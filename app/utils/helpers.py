from datetime import datetime
import pytz
import locale

locale.setlocale(locale.LC_TIME, "es_ES.utf8")  # Puede variar según el sistema operativo

# Definir la zona horaria de Argentina
argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")
fecha_hora_actual = datetime.now(argentina_tz)

# Obtener el nombre del día en español
nombre_dia = fecha_hora_actual.strftime("%A").capitalize()
fecha_hora_actual = fecha_hora_actual.strftime("%Y-%m-%d %H:%M")