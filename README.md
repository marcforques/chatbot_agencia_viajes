# Chatbot inteligente para agencia de viajes

Proyecto de chatbot desarrollado en Python para simular la atención al cliente de una agencia de viajes.

La aplicación permite interpretar la intención del usuario, recomendar destinos tur´siticos a partir de un catálogo propio, analizar el sentimiento de mensajes relacionados con quejas o valoraciones y y gestionar reservas mediante una base de datos local SQLite.


## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Numpy
- FAISS
- Sentence Transformers
- Hugging Face Transformers
- LangChain
- Ollama: Llama 3.2
- SQLite


## Funcionalidades principales

- Interfaz conversacional mediante Streamlit.
- Clasificación semántica de la intención del usuario.
- Recomendación de destinos turísticos usando embeddings y búsqueda vectorial.
- Generación de respuestas naturales con un modelo LLM local mediante Ollama.
- Análisis de sentimiento para mensajes de queja o valoración.
- Uso de datasets sintéticos en formato CSV.
- Gestión de reservas mediante una base de datos SQLite.
- Creación de reservas con número único.
- Consulta de reservas existentes.
- Modificación de reservas.
- Cancelación lógica de reservas mediante cambio de estado.
- Control básico de errores cuando algún componente no está disponible.


## Funcionamiento general

El chatbot recibe un mensaje del usuario desde la interfaz de Streamlit.

Primero, el sistema clasifica la intención del mensaje mediante embeddings generados con Sentence Transformers y búsqueda de similitud con FAISS.

Según la intención detectada, el chatbot puede seguir diferentes flujos:

- Si el usuario busca una recomendación de viaje, se consulta el catálogo de destinos y se genera una respuesta personalizada usando Llama 3.2 mediante Ollama.
- Si el usuario escribe una queja o valoración, se analiza el sentimiento del mensaje con un modelo de Hugging Face.
- Si el usuario quiere crear una reserva, se muestra un formulario y se guarda la información en una base de datos SQLite.
- Si el usuario quiere consultar una reserva, se busca por número de reserva en la base de datos.
- Si el usuario quiere modificar una reserva, se actualizan los datos principales y se cambia su estado a modificada.
- Si el usuario quiere cancelar una reserva, no se elimina de la base de datos, sino que se cambia su estado a cancelada.
- Si el sistema detecta saludos, despedidas o contacto humano, responde con mensajes controlados.

## Estructura del proyecto

```text
chatbot-agencia-viajes/
│
├── chatbot.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── datos_csv/
│   ├── destinos2.csv
│   └── intenciones2.csv
│
└── modelos/
    ├── intencion.py
    ├── recomendacion_destino.py
    ├── sentimientos.py
    └── reservas_db.py
```

## Instalación y ejecución

### 1. Clonar el repositorio
git clone https://github.com/marcforques/chatbot_agencia_viajes.git
cd chatbot_agencia_viajes

### 2. Crear un entorno virtual y activarlo
python -m venv .venv
.venv\Scripts\activate

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Instalar ollama y descargar el modelo
ollama pull llama3.2

### 5. Ejecutar aplicación
streamlit run chatbot.py


## Estado del proyecto

El proyecto se encuentra en una segunda versión funcional.

Actualmente permite probar un flujo completo de chatbot con clasificación de intención, recuperación de información desde un catálogo de destinos, generación de respuestas con un modelo LLM local y gestión básica de reservas mediante SQLite.

## Limitaciones actuales 

- El catálogo de destinos es limitado y está basado en archivos CSV.
- La clasificación de intención depende de los ejemplos incluidos en el dataset.
- El modelo LLM requiere tener Ollama instalado y ejecutándose en local.
- La gestión de reservas es local y no incluye autenticación de usuarios.
- La extracción de datos de la conversación todavía se realiza mediante formularios de Streamlit.
- No incluye todavía una evaluación formal de precisión del clasificador.
- No dispone de base de datos ni sistema de usuarios todavía.


## Mejoras futuras

- Ampliar el dataset de intenciones.
- Añadir más destinos y filtros de búsqueda.
- Incorporar una base de datos en lugar de archivos CSV.
- Añadir métricas de evaluación para la clasificación de intención.
- Mejorar la interfaz visual de Streamlit.
- Mejorar la extracción automática de datos de reserva desde lenguaje natural.
- Añadir una tabla de clientes relacionada con la tabla de reservas.
- Sustituir SQLite por PostgreSQL en una versión más avanzada.
- Añadir respuestas generadas por IA para más tipos de intención.

## Autor

Marc Forqués Isasi

