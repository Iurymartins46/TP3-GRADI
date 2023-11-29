from backend.manipularDataBase import ManipularDataBase
from backend.manipularApiTmdb import ManipularApiTmdb
from backend.servicos import Servicos

dataBase = ManipularDataBase()
api = ManipularApiTmdb()
servico = Servicos()

print("-------------------------------------------------")
#boolean = dataBase.criarDataBase()
#dados = api.obter_informacoes_filme_por_id(565770)
#teste = dataBase.inserirFilmeDataBase(dados_filme=dados)
#print(dataBase.recuperarFilmePorID(1))

servico.popularDataBase()

print(dataBase.recuperarIndiceInvertido())
print("-------------------------------------------------")