from fastapi import FastAPI, Request, HTTPException
import wpp.services as services
import os

TOKEN = os.getenv("TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_URL = os.getenv("WHATSAPP_URL")

app = FastAPI()

@app.get("/bienvenido")
def bienvenido():
    return {"message": "Hola mundo"}

@app.get("/webhook")
def verificar_token(hub_verify_token: str, hub_challenge: str = None):
    try:
        if hub_verify_token == TOKEN and hub_challenge is not None:
            return hub_challenge
        else:
            raise HTTPException(status_code=403, detail="Token incorrecto")
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.post("/webhook")
async def recibir_mensajes(request: Request):
    try:
        body = await request.json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_mensaje_whatsapp(message)

        services.administrar_chatbot(text, number, messageId, name)
        return {"status": "enviado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"no enviado: {str(e)}")