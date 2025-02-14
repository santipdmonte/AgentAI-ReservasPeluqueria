# import whisper
# import io
# from pydub import AudioSegment
# import tempfile
# import requests

# from app.config import ACCESS_TOKEN


# model = whisper.load_model("base")


# # if message.get("type") == "audio":
# #                     media_id = message.get("audio", {}).get("id")


# def audio_to_text(media_id: str) -> str:
#     transcription = None

#     try:
#         # Descargar el audio en bytes
#         audio_bytes = download_audio(media_id)
        
#         # Convertir el audio a formato WAV (se asume que WhatsApp envía OGG)
#         audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="ogg")
        
#         # Guarda el audio en un archivo temporal
#         with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
#             audio_segment.export(tmp.name, format="wav")
#             tmp.flush()
            
#             # Transcribe el audio utilizando Whisper
#             result = model.transcribe(tmp.name)
#             transcription = result.get("text", "")
#             print(f"Transcripción: {transcription}")
    
#     except Exception as e:
#         print(f"Error procesando audio: {e}")

#     return {"status": "success", "transcription": transcription}


# def download_audio(media_id: str) -> bytes:
#     """
#     Descarga el archivo de audio usando el media_id de WhatsApp.
#     """
#     # 1. Solicita la URL del medio
#     media_endpoint = f"https://graph.facebook.com/v16.0/{media_id}"
#     headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
#     response = requests.get(media_endpoint, headers=headers)
#     if response.status_code != 200:
#         raise Exception("Error al obtener la URL del medio")
    
#     media_url = response.json().get("url")
#     if not media_url:
#         raise Exception("No se encontró la URL del medio")
    
#     # 2. Descarga el contenido del archivo de audio
#     media_response = requests.get(media_url)
#     if media_response.status_code != 200:
#         raise Exception("Error al descargar el archivo de audio")
    
#     return media_response.content






