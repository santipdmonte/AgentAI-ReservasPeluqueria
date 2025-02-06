from datetime import datetime
import pytz

# Definir la zona horaria de Argentina
argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")
# Obtener la fecha y hora actual en Argentina
fecha_hora_actual = datetime.now(argentina_tz)
# Obtener el nombre del día en español
nombre_dia = fecha_hora_actual.strftime("%A").capitalize()