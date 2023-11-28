from manipularDataBase import ManipularDataBase

class ValidacaoUsuario:

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
