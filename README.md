# Chatbot inteligente para agencia de viajes

Proyecto de chatbot desarrollado en Python para simular la atención al cliente de una agencia de viajes.

La aplicación permite interpretar la intención del usuario, recomendar destinos tur´siticos a partir de un catálogo propio y analizar el sentimiento de mensajes relacionados con quejas o valoraciones.


## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Numpy
- FAISS
- Sentence Transformers
- Hugging Face Transformers
- LangChain
- Ollama: Llama 3


## Funcionalidades principales

- Interfaz conversacional mediante Streamlit.
- Clasificación semántica de la intención del usuario.
- Recomendación de destinos turísticos usando embeddings y búsqueda vectorial.
- Generación de respuestas naturales con un modelo LLM local.
- Análisis de sentimiento para mensajes de queja o valoración.
- Uso de datasets sintéticos en formato CSV.


## Funcionamiento general

El chatbot recibe un mensaje del usuario desde la interfaz de Streamlit.

Primero, el sistema clasifica la intención del mensaje mediante embeddings generados con Sentence Transformers y búsqueda de similitud con FAISS.

Según la intención detectada, el chatbot puede seguir diferentes flujos:

- Si el usuario busca una recomendación de viaje, se consulta el catálogo de destinos y se genera una respuesta personalizada usando Llama 3.2 mediante Ollama.
- Si el usuario escribe una queja o valoración, se analiza el sentimiento del mensaje con un modelo de Hugging Face.
- Si el usuario solicita contacto humano o realiza un saludo, el sistema responde con mensajes específicos.

## Estructura del proyecto

```text
chatbot-agencia-viajes/
│
├── chatbot.py
├── README.md
├── requirements.txt
│
├── datos_csv/
│   ├── destinos2.csv
│   └── intenciones2.csv
│
└── modelos/
    ├── intencion.py
    ├── recomendacion_destino.py
    └── sentimientos.py
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

El proyecto se encuentra en una primera versión funcional.

Actualmente permite probar un flujo completo de chatbot con clasificación de intención, recuperación de información desde un catálogo de destinos y generación de respuestas con un modelo LLM local.


## Limitaciones actuales 

- El catálogo de destinos es limitado y está basado en archivos CSV.
- La clasificación de intención depende de los ejemplos incluidos en el dataset.
- El modelo LLM requiere tener Ollama instalado y ejecutándose en local.
- No incluye todavía una evaluación formal de precisión del clasificador.
- No dispone de base de datos ni sistema de usuarios todavía.


## Mejoras futuras

- Ampliar el dataset de intenciones.
- Añadir más destinos y filtros de búsqueda.
- Incorporar una base de datos en lugar de archivos CSV.
- Añadir métricas de evaluación para la clasificación de intención.
- Mejorar la interfaz visual de Streamlit.
- Añadir control de errores cuando Ollama no esté disponible.


## Autor

Marc Forqués Isasi

