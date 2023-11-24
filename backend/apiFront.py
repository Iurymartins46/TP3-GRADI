from flask import Flask, request, jsonify
from flask_cors import CORS
from manipularDataBase import ManipularDataBase

app = Flask(__name__)
CORS(app) 

"""
@app.route('/criarUsuario', methods=['POST'])
def criarUsuario():
    email = request.json.get("email")
    senha = request.json.get("senha")
    validacao = Validacao()
    confirmacao,idUsr = validacao.criarContaNovoUsuario(email=email,senha=senha)

    data = {
        "confirmacao": confirmacao,
        "usuario_id": idUsr
    }
    
    '''
    dicionario = dict() 
    dicionario ["confirmacao"] = confirmacao
    dicionario ["usuario_id"] = idUsr '''


    return data, 200


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
    manipularDataBase = ManipularDataBase()
    confirmacao_db = criarDatabase = manipularDataBase.criarDataBase()
    app.run(debug=True)
    manipularDataBase = ManipularDataBase()
