from math import log10

def calcular_tfidf(frase, indice_invertido):
    # Dicionário para armazenar o TF de cada palavra na frase
    tf = {}

    # Conjunto para armazenar documentos únicos
    documentos_unicos = set()

    # Calcula o TF para cada palavra na frase e identifica documentos únicos
    for palavra in frase.split():
        tf[palavra] = tf.get(palavra, 0) + 1
        if palavra in indice_invertido:
            documentos_unicos.update([doc for doc, _ in indice_invertido[palavra]])

    # Número total de documentos
    total_documentos = len(documentos_unicos)
    print(total_documentos)

    # Calcula o TF-IDF para cada palavra na frase
    for palavra, tf_valor in tf.items():
        if palavra in indice_invertido:
            # Calcula o IDF
            idf = log10(total_documentos / len(indice_invertido[palavra]))

            # Calcula o TF-IDF para cada ocorrência da palavra em um documento
            for doc, posicao in indice_invertido[palavra]:
                tfidf = tf_valor * idf
                print(f"Palavra: {palavra}, Documento: {doc}, TF-IDF: {tfidf}")

# Exemplo de uso com chaves tendo diferentes números de valores
indice_invertido = {
    'palavra1': [('doc1', 5), ('doc2', 8)],
    'palavra2': [('doc1', 3), ('doc3', 6), ('doc4', 10)],
    'palavra3': [('doc2', 7), ('doc3', 4), ('doc5', 12)]
}

frase_entrada = "palavra1 palavra2 palavra3"

calcular_tfidf(frase_entrada, indice_invertido)
