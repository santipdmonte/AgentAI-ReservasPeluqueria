from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse
import app.services.wpp_tools as wpp_tools

from app.services.agent_initializer import agent_initializer
from app.config import TOKEN


app = FastAPI(title="Agent de Peluquería", version="1.0")

@app.get("/bienvenido")
def bienvenido():
    return {"message": "Hola mundo"}

@app.get("/test")
def test(
    txt_message: str = None
    ,number: str = "3413918907"
    ):

    result = agent_initializer(number, txt_message)

    return {"message": result}    

@app.get("/webhook", response_class=PlainTextResponse)
async def verificar_token(request: Request):
    try:
        # Obtener los parámetros de la manera correcta
        params = dict(request.query_params)
        token = params.get('hub.verify_token')
        challenge = params.get('hub.challenge')

        # Validar el token y el challenge
        if token == TOKEN and challenge is not None:
            return challenge
        else:
            return PlainTextResponse('Token incorrecto', status_code=403)
            
    except Exception as e:
        return PlainTextResponse(str(e), status_code=403)

# @app.post("/webhook")
# async def recibir_mensajes(
#     request: Request
#     # ,txt_message: str = None
#     ):
#     try:
#         # if txt_message:
#         #     message = txt_message
#         #     agent_answer = agent_initializer("3413918907", message)
#         #     return agent_answer
#         # return {"status": "enviado"}

#         body = await request.json()
#         entry = body['entry'][0]
#         changes = entry['changes'][0]
#         value = changes['value']
#         message = value['messages'][0]
#         number = wpp_tools.replace_start(message['from'])
#         messageId = message['id']
#         contacts = value['contacts'][0]
#         name = contacts['profile']['name']
#         text = wpp_tools.obtener_mensaje_whatsapp(message)


#         text = text.lower() # Mensaje que envio el usuario
#         list = []

#         # Marcar el mensaje como leído
#         list.append(wpp_tools.markRead_Message(messageId))

#         # Enviamos al bot el mensaje del usuario
#         agent_answer = agent_initializer(number, text)

#         # Enviamos la respuesta del bot al usuario
#         listReplyData = wpp_tools.text_message(number, agent_answer)
#         list.append(listReplyData)

#         for item in list:
#             wpp_tools.enviar_mensaje_whatsapp(item)


#         return {"status": "enviado"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"no enviado: {str(e)}")


from fastapi.responses import JSONResponse
import logging
# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/webhook")
async def recibir_mensajes(request: Request):
    try:
        # Obtener y loggear el body completo
        body = await request.json()

        logger.debug(f"\n ========= Mensaje recibido =========================== ")
        logger.debug(f"\n\nMensaje recibido: {body}")

        # Validar estructura básica del mensaje
        if "entry" not in body or not body["entry"]:
            logger.warning("\n\nMensaje recibido sin entradas")
            return JSONResponse(content={"status": "ok"}, status_code=200)

        # Extraer información del mensaje
        try:
            entry = body['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']

            # Verificar si hay mensajes
            if 'messages' not in value:
                logger.info("\n\nMensaje recibido sin contenido de mensajes - podría ser una actualización de estado")
                return JSONResponse(content={"status": "ok"}, status_code=200)

            message = value['messages'][0]
            
            # Procesar la información del mensaje
            number = wpp_tools.replace_start(message['from']) # Reestructura el numero de telefono para que sea compatible
            messageId = message['id']
            contacts = value['contacts'][0]
            name = contacts['profile']['name']
            text = wpp_tools.obtener_mensaje_whatsapp(message)
            
            logger.info(f"\n\nMensaje recibido de {name} ({number}): {text}")

            # Procesar el mensaje
            text = text.lower()
            response_list = []

            # Marcar como leído
            read_response = wpp_tools.markRead_Message(messageId)
            response_list.append(read_response)
            logger.debug(f"\n\nMensaje marcado como leído: {messageId}")

            # Obtener respuesta del bot
            agent_answer = agent_initializer(number, text)
            logger.debug(f"\n\nRespuesta del bot: {agent_answer}")

            # Preparar respuesta para el usuario
            reply_data = wpp_tools.text_message(number, agent_answer)
            response_list.append(reply_data)

            # Enviar mensajes
            for item in response_list:
                result = wpp_tools.enviar_mensaje_whatsapp(item)
                logger.debug(f"\n\nResultado del envío: {result}")

            return JSONResponse(content={"status": "enviado", "message": "Mensaje procesado correctamente"}, status_code=200)

        except KeyError as e:
            logger.warning(f"\n\nEstructura de mensaje inesperada: {str(e)}")
            return JSONResponse(content={"status": "ok"}, status_code=200)

    except Exception as e:
        logger.error(f"\n\nError procesando mensaje: {str(e)}")
        # Log del error completo para debugging
        import traceback
        logger.error(traceback.format_exc())
        
        # En producción, mejor devolver 200 para evitar reintentos de WhatsApp
        return JSONResponse(
            content={
                "status": "error",
                "detail": str(e)
            },
            status_code=200  # Cambiado de 400 a 200 para evitar reintentos
        )  


# python -m uvicorn app.main:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)