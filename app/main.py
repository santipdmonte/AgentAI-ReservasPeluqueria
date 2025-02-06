from fastapi import FastAPI, Request, HTTPException
import app.services.wpp_tools as wpp_tools
import os

from app.services.agent_initialazer import inicializar_agente
from app.config import TOKEN, WHATSAPP_TOKEN, WHATSAPP_URL


app = FastAPI(title="Agent de Peluquería", version="1.0")

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
        number = wpp_tools.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']

        text = wpp_tools.obtener_mensaje_whatsapp(message)

        
        # wpp_tools.administrar_chatbot(text, number, messageId, name)

        text = text.lower() #mensaje que envio el usuario
        list = []
        print("mensaje del usuario: ",text)

        list.append(wpp_tools.markRead_Message(messageId))

        # Enviamos al bot el mensaje del usuario
        body = inicializar_agente(number, text)
        print(body)
        listReplyData = wpp_tools.text_message(number,text)
        list.append(listReplyData)



        return {"status": "enviado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"no enviado: {str(e)}")
        



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)