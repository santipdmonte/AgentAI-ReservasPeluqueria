from app.services.agent import create_agent

from config import BASE_URL

import requests
from langchain_core.messages import HumanMessage

def agent_initializer(number: str, user_input: str):

    phone_number = "3413918906"
    # user_input = "15.30hs"

    app = create_agent()


    # ==== Setup user data ====
    try:
        url = f"{BASE_URL}usuarios/telefono/{phone_number}"
        print(url)

        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            print("Usuario encontrado: ", user_data)

        else:
            user_data = None
            print("Error: ", response.status_code, response.json())

    except requests.RequestException as e:
        print("Error en la solicitud: ", e)

    if user_data:
        name = user_data['nombre']
        user_id = user_data['id']
    else:
        # Crear un nuevo usuario
        name = None
        user_id = None


        
    initial_state = {
        'user_id': user_id,
        'name': name,
        'phone_number': phone_number,
        "messages": [HumanMessage(content=user_input)]
    }

    config = {"configurable": {"thread_id": user_id}}


    print("\n ==================== Inicio Mensaje =================================================")
    print(f"\nUsuario: {user_input}\n")

    # Invocar el grafo
    response = app.invoke(initial_state, config)
    
    # Obtener el último mensaje (respuesta de IA)
    ai_response = response['messages'][-1].content

    print(f"\nAgente: {ai_response}")
    print("\n ==================== Fin mensaje ====================================================")

    return ai_response