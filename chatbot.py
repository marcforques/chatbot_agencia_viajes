import streamlit as st

# Importamos las funciones creadas en los modelos
from modelos.intencion import predecir_intencion
from modelos.recomendacion_destino import responder_consulta_final
from modelos.sentimientos import evaluar_comentario

# Pequeña configuración de la visual de la página
st.set_page_config(page_title="Chatbot para agencia de viajes")
st.title("Chatbot para agencia de viajes")

# Definimos el mensaje inicial del bot
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu agente de viajes virtual. ¿En qué te puedo ayudar hoy?"}
    ]

# Mostramos el historial en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Guardamos lo que escribe el usuario
prompt = st.chat_input("Escribe aquí tu mensaje...")

if prompt:
    # Mostramos el mensaje del usuario en la pantalla
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Procesamineto del bot
    with st.chat_message("assistant"):
        with st.spinner("Analizando tu petición..."):
            
            # Detectamos la intención del usuario
            intencion = predecir_intencion(prompt)
            
            # Según su intención:
            # Si quiere obtener una recomendación del viaje se utiliza la función creada anteriormente para la búsqueda de destinos en la base de datos
            if intencion == "recomendacion_viaje":
                st.info(f"Intención detectada: Búsqueda de viaje. Consultando catálogo...")
                respuesta_final = responder_consulta_final(prompt, st.session_state.messages)
            
            # Si detecta una queja, analiza el sentimiento y responde acorde el tipo de sentimiento
            elif intencion == "queja":
                st.warning(f"Intención detectada: Queja. Analizando sentimiento...")
                sentimiento, seguridad = evaluar_comentario(prompt)
                
                if "NEGATIVO" in sentimiento:
                    respuesta_final = "Lamento muchísimo leer esto. He registrado tu queja, un agente humano te contactará para compensarte. ¿Puedo ayudarte con algo más?"
                elif "NEUTRAL" in sentimiento:
                    respuesta_final = "Gracias por el feedback, seguimos trabajando para mejorar."
                else:
                    respuesta_final = "Nos alegra saber que estás contento con la experiencia, nos vemos pronto."
                    
            elif intencion == "saludo":
                respuesta_final = "¡Hola de nuevo! ¿En qué puedo ayudarte?"
                
            elif intencion == "contacto_humano":
                respuesta_final = "Entiendo. Te estoy transfiriendo con uno de nuestros agentes humanos. Por favor, mantente a la espera un momento..."
                
            else:
                respuesta_final = f"He detectado que tu intención es '{intencion}', pero esa funcionalidad aún está en desarrollo."

            # Mostrar respuesta final simulando escritura
            st.markdown(respuesta_final)
            
    # Guardamos la respuesta en la memoria
    st.session_state.messages.append({"role": "assistant", "content": respuesta_final})