import math

def calcular_tfidf(frase, indice_invertido):
    # Dicionário para armazenar o TF de cada palavra na frase por documento
    tf = {}

    #lista das palavra da frase digitada
    palavras = frase.split(" ")

    valores_unicos = set()

    # Vetor para armazenar os primeiros valores das tuplas
    lista_docs = []

    #cáculo do número de docs no corpus
    # Iterando sobre os valores do dicionário
    for valores_tupla in indice_invertido.values():
        for tupla in valores_tupla:
            primeiro_valor = tupla[0]
            # Verificando se o valor já foi adicionado ao conjunto
            if primeiro_valor not in valores_unicos:
                # Adicionando o valor ao vetor e ao conjunto
                lista_docs.append(primeiro_valor)
                valores_unicos.add(primeiro_valor)

    #num total de documentos no corpus
    total_docs = len(lista_docs)

    """print(total_docs)"""
        
    # Inicializando o dicionário de contagem
    #dicionário que contém o id de cada doc de índece juntamento com cada palavra da frase e quantas vezes aparece
    dic = {num: [(palavra, 0) for palavra in palavras] for num in set(num for tuplas in indice_invertido.values() for num, _ in tuplas)}

    # Preenchendo o dicionário de contagem
    for palavra in palavras:
        for tupla in indice_invertido.get(palavra, []):
            num = tupla[0]
            dic[num][palavras.index(palavra)] = (palavra, dic[num][palavras.index(palavra)][1] + 1)

    """# Exibindo o resultado
    for num, contagens in dic.items():
        print(f"{num}: {contagens}")"""
    
    #cálculo do número de palavras por documento
    # Dicionário para armazenar a contagem do número de palavras por documento
    num_palavras = {num: 0 for num in lista_docs}

    # Contando a ocorrência de cada número
    for palavras, tuplas in indice_invertido.items():
        for tupla in tuplas:
            primeiro_numero = tupla[0]
            if primeiro_numero in num_palavras:
                num_palavras[primeiro_numero] += 1

    """# Exibindo o resultado
    print(num_palavras)"""

    #Cálculo de quantos documentos tem cada termo
    num_contem = {}

    for palavra, tuplas in indice_invertido.items():
        valores_diferentes = set(tupla[0] for tupla in tuplas)
        num_contem[palavra] = len(valores_diferentes)

    """print(num_contem)"""


    #calculo do tf
    for doc_id, contagem in dic.items():
        tf[doc_id] = []
        total_palavras = num_palavras[doc_id]
        
        for palavra, quantidade in contagem:
            frequencia = quantidade / total_palavras if total_palavras > 0 else 0
            tf[doc_id].append((palavra, frequencia))

    """# Exibindo o resultado
    for doc_id, frequencias in tf.items():
        print(f"{doc_id}: {frequencias}")"""
    
    #calculo do idf de cada termo
    idf = {}

    for palavra, num_documentos in num_contem.items():
        idf[palavra] = math.log(total_docs / (1 + num_documentos), 10)  # Adicionando 1 para evitar divisão por zero

    """print(idf)"""

    #calculando o TF-IDF para cada documento
    resultado = {}

    for doc_id, tf_palavras in tf.items():
        resultado[doc_id] = {}
        for palavra, tf_valor in tf_palavras:
            resultado[doc_id][palavra] = tf_valor * idf.get(palavra, 0)

    print(resultado)

# Exemplo de uso com chaves tendo diferentes números de valores
indice_invertido = {
    'palavra1': [(1, 5), (2, 8)],
    'palavra2': [(1, 3), (1,4), (3, 6), (4, 10)],
    'palavra3': [(2, 7), (3, 4), (5, 12)]
}

'''print(indice_invertido['palavra1'][0][0])'''

frase_entrada = "palavra1 palavra2"

calcular_tfidf(frase_entrada, indice_invertido)
