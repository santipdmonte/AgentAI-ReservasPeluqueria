from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse
import app.utils.wpp_tools as wpp_tools
from mangum import Mangum

from app.services.agent_initializer import agent_initializer
from app.routes import events
# from app.utils.audio_to_text import audio_to_text
from app.config import TOKEN


app = FastAPI(title="Agent de Peluquería", version="1.0")
app.include_router(events.router)

handler = Mangum(app)


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


from fastapi.responses import JSONResponse
import logging
# Configurar logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("langchain").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

@app.post("/webhook")
async def recibir_mensajes(request: Request):
    try:
        # Obtener y loggear el body completo
        body = await request.json()

        print(f"\n========= Mensaje recibido =========================== ")
        print(f"\nMensaje recibido: \n{body}\n")

        # Validar estructura básica del mensaje
        if "entry" not in body or not body["entry"]:
            logger.warning("\n - Mensaje recibido sin entradas\n")
            return JSONResponse(content={"status": "ok"}, status_code=200)

        # Extraer información del mensaje
        try:
            entry = body['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']

            # Verificar si hay mensajes
            if 'messages' not in value:
                logger.warning("\nMensaje recibido sin contenido de mensajes - podría ser una actualización de estado\n")
                return JSONResponse(content={"status": "ok"}, status_code=200)

            # # Verificar si hay mensajes de audio
            # if message.get("type") == "audio":
            #     media_id = message.get("audio", {}).get("id")
            #     print(f"\nMensaje de audio recibido: {media_id}\n")
            #     logger.warning("\nEl mensaje recibido es un audio\n")
            #     return JSONResponse(content={"status": "ok"}, status_code=200)
            #     # message = audio_to_text(media_id)
            # else:
                
            message = value['messages'][0]
            
            # Procesar la información del mensaje
            number = wpp_tools.replace_start(message['from']) # Reestructura el numero de telefono para que sea compatible
            messageId = message['id']
            contacts = value['contacts'][0]
            name = contacts['profile']['name']
            text = wpp_tools.obtener_mensaje_whatsapp(message)
            
            print(f"\nMensaje recibido de {name} ({number}): {text}\n")

            # Procesar el mensaje
            text = text.lower()
            response_list = []

            # Marcar como leído
            mark_as_read = wpp_tools.markRead_Message(messageId)
            result = wpp_tools.send_to_whatsapp(mark_as_read)
            print(f"\nMensaje ({messageId}) marcado como leído: {result}\n")
            # response_list.append(read_response)

            # Obtener respuesta del bot
            agent_answer = agent_initializer(number, text)
            print(f"\nRespuesta del bot: {agent_answer}\n")

            # Preparar respuesta para el usuario
            reply_data = wpp_tools.text_message(number, agent_answer)
            response_list.append(reply_data)

            # Enviar mensajes
            result = wpp_tools.send_to_whatsapp(reply_data)
            print(f"\nResultado del envío: {result}\n")

            return JSONResponse(content={"status": "enviado", "message": "Mensaje procesado correctamente"}, status_code=200)

        except KeyError as e:
            # Enviar mensaje de error
            msj_error = "Actualmente no podemos procesar tu mensaje, vuelve a intentarlo mas tarde :("
            reply_data = wpp_tools.text_message(number, msj_error)
            response_list.append(reply_data)

            logger.warning(f"\n\nEstructura de mensaje inesperada: {str(e)}")
            return JSONResponse(content={"status": "ok"}, status_code=200)
    


    except Exception as e:
        logger.error(f"\nError procesando mensaje: {str(e)}\n")
        # Log del error completo para debugging
        import traceback
        logger.error(traceback.format_exc())

        # Enviar mensaje de error
        msj_error = "Actualmente no podemos procesar tu mensaje, vuelve a intentarlo mas tarde :("
        reply_data = wpp_tools.text_message(number, msj_error)
        response_list.append(reply_data)
        
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