from fastapi import APIRouter
import requests
from app.config import BASE_URL
from app.utils.reminder import enviar_recordatorio 
import json

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post("/generar_horarios")
async def generar_horarios_semanales():
    
    try:   
        
        requests.post(f"{BASE_URL}/horarios/generar_horarios")

        return {
        "statusCode": 200,
        "body": json.dumps("Horarios generados con exito")
        }
    
    except Exception as e:
        print("Error interno:", e)
        return {
            "statusCode": 500,
            "body": f"Error interno: {str(e)}"
        }
    
    
@router.post("/recordatorios")
async def enviar_recordatorios():
    
    try:   
        
        enviar_recordatorio()

        return {
        "statusCode": 200,
        "body": json.dumps("Recordatorios enviados con exito")
        }
    
    except Exception as e:
        print("Error interno:", e)
        return {
            "statusCode": 500,
            "body": f"Error interno: {str(e)}"
        }


