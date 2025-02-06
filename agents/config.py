import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

DB_URI = os.getenv("DATABASE_URL") 

BASE_URL = "http://localhost:8000/"


from datetime import datetime
import pytz

# Definir la zona horaria de Argentina
argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")
# Obtener la fecha y hora actual en Argentina
fecha_hora_actual = datetime.now(argentina_tz)
# Obtener el nombre del día en español
nombre_dia = fecha_hora_actual.strftime("%A").capitalize()