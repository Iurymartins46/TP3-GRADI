from flask import Flask, request, jsonify
from flask_cors import CORS
from servicos import Servicos

app = Flask(__name__)
CORS(app) 


@app.route('/criarNovoUsuario', methods=['POST'])
def criarNovoUsuario():
    email = request.json.get("email")
    senha = request.json.get("senha")
    servicos = Servicos()
    confirmacao,idUsr = servicos.criarNovoUsuario(email=email,senha=senha)

    data = {
        "confirmacao": confirmacao,
        "usuario_id": idUsr
    }
    
    '''
    dicionario = dict() 
    dicionario ["confirmacao"] = confirmacao
    dicionario ["usuario_id"] = idUsr '''


    return data, 200


@app.route('/realizarLogin', methods=['POST'])
def realizarLogin():
    email = request.json.get("email")
    senha = request.json.get("senha")
    servicos = Servicos()
    confirmacao,idUsr = servicos.realizarLogin(email=email,senha=senha)
    data = {
        "confirmacao": confirmacao,
        "usuario_id": idUsr 
    }

    return data, 200


@app.route('/pesquisarFilme', methods=['GET'])
def pesquisarFilme():
    string = request.json.get("string")
    recebelista = Servicos.pesquisarFilme(string=string)
    return recebelista, 200

@app.route('/adicionarFilme', methods=['POST'])
def adicionarFilme():
    id = request.json.get("id")
    titulo = request.json.get("titulo")
    generos = request.json.get("generos")
    orcamento = request.json.get("orcamento")
    receita = request.json.get("receita")
    data_lancamento = request.json.get("data_lancamento")
    tempo_duracao = request.json.get("tempo_duracao")
    slogan = request.json.get("slogan")
    popularidade = request.json.get("popularidade")
    total_votos = request.json.get("total_votos")
    media_votos = request.json.get("media_votos")
    poster_path = request.json.get("poster_path")
    sinopse = request.json.get("sinopse")

    dicionario = dict() 
    dicionario ["id"] = id
    dicionario ["titulo"]= titulo
    dicionario ["generos"] = {i: valor for i, valor in enumerate(generos)}
    dicionario ["orcamento"]= orcamento
    dicionario ["receita"]= receita
    dicionario ["data_lancamento"]= data_lancamento
    dicionario ["tempo_duracao"]= tempo_duracao
    dicionario ["slogan"]= slogan
    dicionario ["popularidade"]= popularidade
    dicionario ["total_votos"]= total_votos
    dicionario ["media_votos"]= media_votos
    dicionario ["poster_path"]= poster_path
    dicionario ["sinopse"]= sinopse
    
    insereFilme = Servicos.adicionarFilme(dicionario)
    
    return insereFilme, 200

if __name__ == '__main__':
    app.run(debug=True)
