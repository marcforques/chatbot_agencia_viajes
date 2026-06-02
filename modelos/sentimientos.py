from transformers import pipeline

# Cargamos un modelo Bert para el análisis de sentimientos
analizador_sentimiento = pipeline(
    "sentiment-analysis", 
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# Definimos una función para analizar el sentimineto del mensaje según las estrellas obtenidas del modelo Bert
def evaluar_comentario(texto_usuario):
    """
    Analiza el texto y devuelve si es POSITIVO, NEGATIVO o NEUTRAL,
    junto con el porcentaje de seguridad de la red neuronal.
    """
    # El pipeline devuelve una lista con un diccionario
    resultado = analizador_sentimiento(texto_usuario)[0]
    etiqueta = resultado['label']
    confianza = resultado['score']
    
    # Extraemos el número de estrellas
    estrellas = int(etiqueta.split(' ')[0])
    
    # Lógica de negocio para la agencia de viajes
    if estrellas <= 2:
        sentimiento = "NEGATIVO"
    elif estrellas == 3:
        sentimiento = "NEUTRAL"
    else:
        sentimiento = "POSITIVO"
        
    return sentimiento, confianza

