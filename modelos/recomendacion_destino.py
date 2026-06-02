from pathlib import Path

import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Definimos la ruta de los archivos csv
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "datos_csv"

# Cargamos el modelo de embeddings 
modelo_embeddings = SentenceTransformer('all-MiniLM-L6-v2') 

# Cargamos destinos
df_destinos = pd.read_csv(DATA_DIR / "destinos2.csv")
textos_destinos = df_destinos['descripcion_corta'].tolist()

# Vectorizamos
embeddings_destinos = modelo_embeddings.encode(textos_destinos)

# Convertimos a float32 
embeddings_destinos = np.array(embeddings_destinos).astype('float32')

# Creación del índice faiss
indice_destinos = faiss.IndexFlatL2(embeddings_destinos.shape[1])
indice_destinos.add(embeddings_destinos)

# Creamos una función para obtener contexto
def obtener_contexto(consulta, k=3):
    vector_consulta = modelo_embeddings.encode([consulta]).astype('float32')
    distancias, indices = indice_destinos.search(vector_consulta, k)
    
    contexto_formateado = ""
    for idx in indices[0]:
        row = df_destinos.iloc[idx]
        contexto_formateado += f"- Destino: {row['destino']}, País: {row['pais']}. Descripción: {row['descripcion_corta']}\n"
    return contexto_formateado

# Creamos una plantilla para el prompt con el objetivo de evitar fallos innecesarios
plantilla_prompt = """
Eres un experto agente de viajes de una agencia de viajes. 
Tú misión es recomendar destinos basados en el contexto proporcionado, recordando que estás hablando con el usuario.

REGLAS CRÍTICAS:
1. Si el usuario pide una región geográfica (ej. Europa, Asia), verifica que los destinos del contexto pertenezcan a esa región.
2. Si un destino del contexto NO cumple con los requisitos del usuario (geografía, clima, presupuesto), IGNÓRALO y no lo menciones.
3. Si ninguno de los destinos encaja, responde amablemente que no tienes opciones exactas ahora mismo.
4. Responde de forma muy atractiva y profesional en español.
 

HISTORIAL DE CONVERSACIÓN RECIENTE:
{historial}

CONTEXTO DE NUESTRO CATÁLOGO:
{contexto}

PREGUNTA DEL CLIENTE: 
{pregunta}

RESPUESTA DEL AGENTE:
"""

# Creamos el prompt que le pasaremos al modelo
prompt_entrenado = PromptTemplate(
    input_variables=["historial", "contexto", "pregunta"],
    template=plantilla_prompt
)

# Creamos la función de respuesta del modelo
def responder_consulta_final(pregunta_usuario, historial_chat):
    # Obtenemos los datos que necesitas para la pregunta del usuario
    contexto = obtener_contexto(pregunta_usuario)
    
    # Se añaden los últimos 4 mensajes de la conversación formateados como historial
    historial_texto = ""
    for mensaje in historial_chat[-4:]:
        rol = "Usuario" if mensaje["role"] == "user" else "Agente"
        historial_texto += f"{rol}: {mensaje['content']}\n"

    # Se crea el prompt con el contenido obtenido
    prompt_final = prompt_entrenado.format(historial=historial_texto, contexto=contexto, pregunta=pregunta_usuario)
    
    # Inicializamos el LLM  
    llm = Ollama(model="llama3.2")
                 
    # Generamos la respuesta final
    respuesta = llm.invoke(prompt_final)
    return respuesta
