from pathlib import Path

import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Definimos la ruta de los archivos csv
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "datos_csv"

# Cargamos el modelo
modelo_embeddings = SentenceTransformer('all-MiniLM-L6-v2') 

# Cargamos tu dataset
df_intenciones = pd.read_csv(DATA_DIR / "intenciones2.csv")
textos = df_intenciones['texto'].tolist()
etiquetas = df_intenciones['intencion'].tolist()

# Vectorizamos
embeddings = modelo_embeddings.encode(textos)

# Convertimos a float32 
embeddings = np.array(embeddings).astype('float32')

# Creación del índice faiss
dimension = embeddings.shape[1] 

# Utilizamos faiss.IndexFlatL2 para la búsqueda 
indice_faiss = faiss.IndexFlatL2(dimension)
indice_faiss.add(embeddings)

# Definimos la función que vectoriza el texto del usuario y busca la intención más cercana en el índice faiss
def predecir_intencion(mensaje_usuario):

    # Se vectoriza la entrada del usuario
    vector_usuario = modelo_embeddings.encode([mensaje_usuario])
    vector_usuario = np.array(vector_usuario).astype('float32')
    
    # se busca en FAISS el vecino más cercano
    distancias, indices = indice_faiss.search(vector_usuario, k=1)
    
    # Se obtiene la etiqueta que corresponde
    indice_ganador = indices[0][0]
    intencion_detectada = etiquetas[indice_ganador]
    
    return intencion_detectada
