import requests
from langchain_core.messages import HumanMessage
from datetime import datetime

from app.services.agente_user.agent_user import create_agent
from app.services.agente_admin.agent_admin import create_agent_admin
from app.config import BASE_URL



def agent_initializer(phone_number: str, user_input: str):


    # ==== Setup user data ====
    try:

        url = f"{BASE_URL}usuarios/telefono/{phone_number}"
        print(f"\n\n URL: {url}")
        response = requests.get(url)
        print(response.json())
        if response.status_code == 200:
            user_data = response.json()
            print("\n\nUsuario encontrado: ", user_data)
        else:
            user_data = None
            print(f"\n\nNo se encontro usuario con el numero: {phone_number}", response.status_code, response.json())

    except requests.RequestException as e:
        user_data = None
        print(f"\n\nError en la solicitud ({url}): ", e)

    if user_data:
        name = user_data['nombre']
        user_id = user_data['id']
    else:
        # Crear un nuevo usuario
        name = None
        user_id = None


    # Set Admin or User agent
    if phone_number == '7777777':     # Replace for user_data['rol'] == 'admin' 
        app = create_agent_admin()
    else:
        app = create_agent()
        

    initial_state = {
        'user_id': user_id,
        'name': name,
        'phone_number': phone_number,
        "messages": [HumanMessage(content=user_input)]
    }

    fecha_hora_actual = datetime.now().strftime('%Y%m%d')
    thread_id = f"{phone_number} | {fecha_hora_actual}"
    config = {"configurable": {"thread_id": thread_id, "recursion_limit": 10}}


    print("\n ==================== Inicio Mensaje =================================================")
    print(f"\nUsuario: {user_input}\n")

    # Invocar el grafo
    response = app.invoke(initial_state, config)
    
    # Obtener el último mensaje (respuesta de IA)
    ai_response = response['messages'][-1].content

    print(f"\nAgente: {ai_response}")
    print("\n ==================== Fin mensaje ====================================================")

    return ai_response