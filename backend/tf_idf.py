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

    # Inicializando o dicionário de contagem
    #dicionário que contém o id de cada doc de índece juntamento com cada palavra da frase e quantas vezes aparece
    dic = {num: [(palavra, 0) for palavra in palavras] for num in set(num for tuplas in indice_invertido.values() for num, _ in tuplas)}

    # Preenchendo o dicionário de contagem
    for palavra in palavras:
        for tupla in indice_invertido.get(palavra, []):
            num = tupla[0]
            dic[num][palavras.index(palavra)] = (palavra, dic[num][palavras.index(palavra)][1] + 1)

    #cálculo do número de palavras por documento
    # Dicionário para armazenar a contagem do número de palavras por documento
    num_palavras = {num: 0 for num in lista_docs}

    # Contando a ocorrência de cada número
    for palavras, tuplas in indice_invertido.items():
        for tupla in tuplas:
            primeiro_numero = tupla[0]
            if primeiro_numero in num_palavras:
                num_palavras[primeiro_numero] += 1

    #Cálculo de quantos documentos tem cada termo
    num_contem = {}

    for palavra, tuplas in indice_invertido.items():
        valores_diferentes = set(tupla[0] for tupla in tuplas)
        num_contem[palavra] = len(valores_diferentes)

    #calculo do tf
    for doc_id, contagem in dic.items():
        tf[doc_id] = []
        total_palavras = num_palavras[doc_id]
        
        for palavra, quantidade in contagem:
            frequencia = quantidade / total_palavras if total_palavras > 0 else 0
            tf[doc_id].append((palavra, frequencia))


    #calculo do idf de cada termo
    idf = {}

    for palavra, num_documentos in num_contem.items():

        idf[palavra] = abs(math.log(total_docs / (1 + num_documentos), 10))  # Adicionando 1 para evitar divisão por zero

    resultado = {}

    for doc_id, tf_palavras in tf.items():
        resultado[doc_id] = {}
        for palavra, tf_valor in tf_palavras:
            resultado[doc_id][palavra] = tf_valor * idf.get(palavra, 0)
    dados = {}
    for key, value in resultado.items():
        tf_idf = 0
        for k, v in value.items():
            tf_idf += v
        dados[key] = tf_idf / len(value)

    dados = dict(sorted(dados.items(), key=lambda item: item[1], reverse=True))
    dados = {chave: valor for chave, valor in dados.items() if valor > 0}
    dados = list(dados.keys())
    print (dados)
    # Seleciona os 10 primeiros elementos da lista
    if len(dados) > 10:
        dados = dados[:10]
        return dados
    return dados

