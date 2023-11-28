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
"""

@app.route('/fazerLogin', methods=['POST'])
def realizarLogin():
    email = request.json.get("email")
    senha = request.json.get("senha")
    validacao = Validacao()
    confirmacao,idUsr = validacao.realizarLogin(email=email,senha=senha)
    data = {
        "confirmacao": confirmacao,
        "usuario_id": idUsr 
    }

    return data, 200


@app.route('/listarDiariosPorTag', methods=['GET'])
def listarDiariosPorTag():
    manipularDataBase = ManipularDataBase()
    usuario_id = request.json.get("usuario_id")
    tag = request.json.get("tag")
    recebelista = manipularDataBase.listarDiariosPorTag(usuario_id=usuario_id,tag=tag)
    return recebelista, 200
"""
if __name__ == '__main__':
    app.run(debug=True)
