from backend.manipularDataBase import ManipularDataBase
from backend.manipularApiTmdb import ManipularApiTmdb

dataBase = ManipularDataBase()
api = ManipularApiTmdb()
print("-------------------------------------------------")
boolean = dataBase.criarDataBase()
dados = api.obter_informacoes_filme_por_id(565770)
teste = dataBase.inserirFilmeDataBase(dados_filme=dados)
print(teste)

print("-------------------------------------------------")