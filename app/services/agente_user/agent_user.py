import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.postgres import PostgresSaver

from psycopg_pool import ConnectionPool

from app.services.schemas import State
from app.services.agente_user.prompts_user import get_formatted_messages
from app.services.tools.tools_reservas import crear_reserva, cancelar_reserva, modificar_reserva, obtener_reservas_del_cliente
from app.services.tools.tools_usuarios import modificar_nombre_usuario, crear_usuario, historial_usuario
from app.services.tools.tools_horarios import encontrar_horarios_disponibles

from app.config import OPENAI_API_KEY, LANGCHAIN_API_KEY, DB_URI  



def create_agent():

    # ==== Set API keys ====
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    os.environ['LANGCHAIN_API_KEY'] = LANGCHAIN_API_KEY

    # ==== Nodes ====
    def call_model(state: State):

        formatted_messages = get_formatted_messages(state, model)

        # Call the model with formatted messages
        response = bound_model.invoke(formatted_messages)
        return {"messages": response}


    #  ==== Conditional Edges ====
    def should_continue(state: State):
        """Return the next node to execute."""

        last_message = state["messages"][-1]

        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return END
        
        # Otherwise if there is, we continue
        return "action"
    

    # ==== Compile Workflow ====
    tools = [crear_reserva, cancelar_reserva, modificar_reserva, obtener_reservas_del_cliente, encontrar_horarios_disponibles, \
            crear_usuario, historial_usuario, modificar_nombre_usuario]
    tool_node = ToolNode(tools)
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatOpenAI(model="gpt-4o")
    bound_model = model.bind_tools(tools)
    workflow = StateGraph(State)


    # Define Nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("action", tool_node)

    # Define Edges
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(     # Conditional Edge
        "agent",                            # Desde este nodo
        should_continue,                    # Nodo controlador
        ["action", END],                    # Posibles nodos a continuar
    )
    workflow.add_edge("action", "agent")
    

    # ==== Checkpointer ====
    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
    }

    pool = ConnectionPool(
        conninfo=DB_URI,
        max_size=10,
        kwargs=connection_kwargs,
    )
        
    checkpointer = PostgresSaver(pool)
    # checkpointer.setup()


    return workflow.compile(checkpointer=checkpointer)


    
    # ==== Chat Loop ====
    try:
        while True:
            try:
                user_input = input("\nHuman: ")
                
                if user_input.lower() in ['salir', 'exit', 'q']:
                    print("Saliendo del chat...")
                    break
                
                # Validar entrada
                if not user_input.strip():
                    print("Por favor, escribe un mensaje.")
                    continue

                initial_state = {
                    'user_id': user_id,
                    'name': name,
                    'phone_number': phone_number,
                    "messages": [HumanMessage(content=user_input)]
                }

                # Ejecutar flujo
                events = app.stream(
                    initial_state,
                    config,
                    stream_mode="values"
                )


                #     for event in events:
                #         event["messages"][-1].pretty_print()

                # Mostrar respuestas
                for event in events:
                    if 'messages' in event and event['messages']:
                        assistant_messages = [
                            msg for msg in event['messages'] 
                            if msg.type != 'human'
                        ]
                        
                        if assistant_messages:
                            print("\nAsistente:", assistant_messages[-1].content)

            except Exception as e:
                print(f"Error en la conversación: {e}")
                continue

    except KeyboardInterrupt:
        print("\nChat interrumpido por el usuario.")

