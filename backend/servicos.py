from manipularDataBase import ManipularDataBase
from manipularApiTmdb import ManipularApiTmdb
from indiceInvertido import IndiceInvertido
class Servicos:

    # return True, usuario_id; Se as credenciais estiverem certas
    # return False, None; Se as credenciais estiverem erradas
    def realizarLogin(self, email, senha):
        email = email.strip()
        senha = senha.strip()
        dataBase = ManipularDataBase()
        login = dataBase.pesquisarUsuarioPorSenhaEmail(email=email, senha=senha)
        if login:
            return True, login
        else:
            return False, None
    
    #return False, None; Caso ja tenha um usario com as mesmas credenciais
    #return True, usuario_id; Caso foi possivel criar o novo usuario
    def criarNovoUsuario(self, email, senha):
        email = email.strip()
        senha = senha.strip()
        dataBase = ManipularDataBase()
        login = dataBase.pesquisarUsuarioPorSenhaEmail(email=email, senha=senha)
        if login:
            return False, None
        else:
            dataBase.criarUsuario(email=email, senha=senha)
            #Como a consulta retorna o id do proximo usuario, subtrair 1 para pegar o id do usuario adicionado
            usuario_id = dataBase.proximoIdUsuario() - 1
            return True, usuario_id
        
    def popularDataBase(self):
        id_tmdb_filmes = [19995, 76600, 872585, 299054, 670292, 678512, 609681, 565770, 
                          695721, 268896, 601, 667538, 634649, 447365, 299536, 569094, 
                          315162, 354912, 577922, 122, 157336, 361743, 22, 588228, 
                          198663, 72190, 262500, 284054, 429351, 406759, 137113, 399579, 
                          17654, 44833, 438631, 428078, 6479, 346698, 1075794, 118340]
        
        dataBase = ManipularDataBase()
        api = ManipularApiTmdb()
        dataBase.criarDataBase()
        teste = []
        for id in id_tmdb_filmes:
            dados = api.obter_informacoes_filme_por_id(id)
            dataBase.inserirFilmeDataBase(dados_filme=dados)
            teste.append(dados['sinopse'])
        indice = IndiceInvertido(teste)

       # print(type(indice.invIndex))
        dataBase.inserirIndiceInvertido(indice.invIndex)
