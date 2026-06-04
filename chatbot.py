import streamlit as st

# Importamos las funciones creadas en los modelos
from modelos.intencion import predecir_intencion
from modelos.recomendacion_destino import responder_consulta_final
from modelos.sentimientos import evaluar_comentario
from modelos.reservas_db import inicializar_db, crear_reserva, consultar_reserva, modificar_reserva, cancelar_reserva

# Inicializamos la base da datos
inicializar_db()

# Pequeña configuración de la visual de la página
st.set_page_config(page_title="Chatbot para agencia de viajes")
st.title("Chatbot para agencia de viajes")

# Definimos el mensaje inicial del bot
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu agente de viajes virtual. ¿En qué te puedo ayudar hoy?"}
    ]

# Añadimos el estado para elegir el formulario
if "accion_reserva" not in st.session_state:
    st.session_state.accion_reserva = None

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
            
            # Según la intención detectada:
            if intencion == "recomendacion_viaje":
                st.info("Intención detectada: recomendación de viaje.")
                
                try:
                    respuesta_final = responder_consulta_final(prompt, st.session_state.messages)
                except Exception:
                    respuesta_final = (
                        "Ahora mismo no puedo generar una recomendación automática. "
                        "Comprueba que Ollama esté abierto y que el modelo llama3.2 esté instalado."
                    )

            elif intencion == "queja":
                st.warning("Intención detectada: queja o valoración.")
                
                try:
                    sentimiento, seguridad = evaluar_comentario(prompt)

                    if sentimiento == "NEGATIVO":
                        respuesta_final = (
                            "Lamento que hayas tenido una mala experiencia. "
                            "He registrado tu comentario como una incidencia y un agente de la agencia debería revisarlo."
                        )
                    elif sentimiento == "NEUTRAL":
                        respuesta_final = (
                            "Gracias por tu comentario. Lo tendremos en cuenta para mejorar la experiencia del cliente."
                        )
                    else:
                        respuesta_final = (
                            "Nos alegra saber que tu experiencia ha sido positiva. "
                            "Gracias por compartir tu valoración."
                        )

                except Exception:
                    respuesta_final = (
                        "He detectado que quieres comunicar una queja o valoración, "
                        "pero ahora mismo no he podido analizar el sentimiento del mensaje."
                    )

            elif intencion == "saludo":
                st.info("Intención detectada: saludo.")
                respuesta_final = (
                    "¡Hola! Soy el asistente virtual de la agencia de viajes. "
                    "Puedo ayudarte a buscar destinos, gestionar reservas o contactar con un agente."
                )

            elif intencion == "despedida":
                st.info("Intención detectada: despedida.")
                respuesta_final = (
                    "Gracias por contactar con la agencia. "
                    "Espero haberte ayudado. ¡Que tengas un buen viaje!"
                )

            elif intencion == "reserva":
                st.info("Intención detectada: creación de reserva.")
                st.session_state.accion_reserva = "crear"

                respuesta_final = (
                    "Perfecto. Puedo ayudarte a crear una reserva. "
                    "Completa el formulario que aparece debajo del chat."
                )

            elif intencion == "consulta_reserva":
                st.info("Intención detectada: consulta de reserva.")
                st.session_state.accion_reserva = "consultar"

                respuesta_final = (
                    "Indícame el número de reserva en el formulario para consultar los datos."
                )

            elif intencion == "modificar_reserva":
                st.info("Intención detectada: modificación de reserva.")
                st.session_state.accion_reserva = "modificar"

                respuesta_final = (
                    "Puedo ayudarte a modificar una reserva. "
                    "Introduce el número de reserva y los nuevos datos en el formulario."
                )

            elif intencion == "cancelacion":
                st.info("Intención detectada: cancelación de reserva.")
                st.session_state.accion_reserva = "cancelar"

                respuesta_final = (
                    "Puedo ayudarte a cancelar una reserva. "
                    "Introduce el número de reserva en el formulario."
                )

            elif intencion == "contacto_humano":
                st.info("Intención detectada: contacto humano.")
                respuesta_final = (
                    "Entiendo. Te derivaría con un agente humano de la agencia para recibir atención personalizada."
                )

            else:
                st.info("Intención no reconocida con suficiente claridad.")
                respuesta_final = (
                    "No he entendido del todo tu solicitud. "
                    "Puedes pedirme una recomendación de viaje, consultar una reserva, cancelar una reserva o contactar con un agente."
                )

            # Mostrar respuesta final simulando escritura
            st.markdown(respuesta_final)
            
    # Guardamos la respuesta en la memoria
    st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
    

st.divider()

# Creamos los formularios según la acción detectada
accion_reserva = st.session_state.get("accion_reserva")

if accion_reserva == "crear":
    st.subheader("Crear nueva reserva")

    with st.form("form_crear_reserva"):
        nombre_cliente = st.text_input("Nombre del cliente")
        destino = st.text_input("Destino")
        fecha_salida = st.date_input("Fecha de salida")
        numero_personas = st.number_input(
            "Número de personas",
            min_value=1,
            step=1
        )
        
        enviar = st.form_submit_button("Crear reserva")

        if enviar:
            if not nombre_cliente or not destino:
                st.error("Debes indicar el nombre del cliente y el destino.")
            else:
                numero_reserva = crear_reserva(
                    nombre_cliente=nombre_cliente,
                    destino=destino,
                    fecha_salida=str(fecha_salida),
                    numero_personas=int(numero_personas),
                )

                st.success(f"Reserva creada correctamente. Número de reserva: {numero_reserva}")
                st.session_state.accion_reserva = None
                
                
elif accion_reserva == "consultar":
    st.subheader("Consultar reserva")

    with st.form("form_consultar_reserva"):
        numero_reserva = st.text_input("Número de reserva")

        enviar = st.form_submit_button("Consultar reserva")

        if enviar:
            reserva = consultar_reserva(numero_reserva)

            if reserva is None:
                st.error("No se ha encontrado ninguna reserva con ese número.")
            else:
                st.success("Reserva encontrada")
                st.write(f"**Número de reserva:** {reserva['numero_reserva']}")
                st.write(f"**Cliente:** {reserva['nombre_cliente']}")
                st.write(f"**Destino:** {reserva['destino']}")
                st.write(f"**Fecha de salida:** {reserva['fecha_salida']}")
                st.write(f"**Número de personas:** {reserva['numero_personas']}")
                st.write(f"**Estado:** {reserva['estado']}")

  
elif accion_reserva == "modificar":
    st.subheader("Modificar reserva")

    with st.form("form_modificar_reserva"):
        numero_reserva = st.text_input("Número de reserva")
        nuevo_destino = st.text_input("Nuevo destino")
        nueva_fecha_salida = st.date_input("Nueva fecha de salida")
        nuevo_numero_personas = st.number_input(
            "Nuevo número de personas",
            min_value=1,
            step=1
        )

        enviar = st.form_submit_button("Modificar reserva")

        if enviar:
            modificada = modificar_reserva(
                numero_reserva=numero_reserva,
                nuevo_destino=nuevo_destino,
                nueva_fecha_salida=str(nueva_fecha_salida),
                nuevo_numero_personas=int(nuevo_numero_personas),
            )

            if modificada:
                st.success("Reserva modificada correctamente.")
                st.session_state.accion_reserva = None
            else:
                st.error("No se ha podido modificar la reserva. Revisa el número o el estado de la reserva.")

elif accion_reserva == "cancelar":
    st.subheader("Cancelar reserva")

    with st.form("form_cancelar_reserva"):
        numero_reserva = st.text_input("Número de reserva")

        enviar = st.form_submit_button("Cancelar reserva")

        if enviar:
            cancelada = cancelar_reserva(numero_reserva)

            if cancelada:
                st.success("Reserva cancelada correctamente.")
                st.session_state.accion_reserva = None
            else:
                st.error("No se ha podido cancelar la reserva. Revisa el número o puede que ya esté cancelada.")