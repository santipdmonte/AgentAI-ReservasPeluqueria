from fastapi import FastAPI, Request, HTTPException, Query
import app.services.wpp_tools as wpp_tools

from app.services.agent_initializer import agent_initializer
from app.config import TOKEN


app = FastAPI(title="Agent de Peluquería", version="1.0")

@app.get("/bienvenido")
def bienvenido():
    return {"message": "Hola mundo"}

@app.get("/test")
def test():

    result = agent_initializer(222, "si, 18hs")

    return {"message": result}    

# @app.get("/webhook")
# def verificar_token(
#         request: Request,
#         # hub_verify_token: str = Query(..., alias="hub.verify_token"),
#         # hub_challenge: str = Query(..., alias="hub.challenge")
#         # hub_verify_token: str, 
#         # hub_challenge: str = None
# ):

#     # Get query parameters using their exact names from Facebook
#     verify_token = request.query_params.get("hub.verify_token")
#     challenge = request.query_params.get("hub.challenge")

#     try:
#         if verify_token != TOKEN:
#             raise HTTPException(status_code=403, detail="Token incorrecto")
#         if challenge is None:
#             raise HTTPException(status_code=403, detail="hub_challenge is null")
#         return challenge
#     except Exception as e:
#         raise HTTPException(status_code=403, detail=str(e))

@app.get("/webhook", response_class=PlainTextResponse)
async def verificar_token(request: Request):
    try:
        # Obtener los parámetros de la manera correcta
        params = dict(request.query_params)
        token = params.get('hub.verify_token')
        challenge = params.get('hub.challenge')

        # Validar el token y el challenge
        if token == sett.token and challenge is not None:
            return challenge
        else:
            return PlainTextResponse('Token incorrecto', status_code=403)
            
    except Exception as e:
        return PlainTextResponse(str(e), status_code=403)

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
        print("Mensaje del usuario: ",text)

        list.append(wpp_tools.markRead_Message(messageId))

        # Enviamos al bot el mensaje del usuario
        agent_answer = agent_initializer(number, text)
        print(f"Mensaje de IA: {agent_answer}")
        listReplyData = wpp_tools.text_message(number,text)
        list.append(listReplyData)


        return {"status": "enviado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"no enviado: {str(e)}")
        


# python -m uvicorn app.main:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)