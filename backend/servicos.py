from manipularDataBase import ManipularDataBase
from manipularApiTmdb import ManipularApiTmdb
from indiceInvertido import IndiceInvertido
from tf_idf import *

import string
from unidecode import unidecode
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

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
        teste = {}
        for id in id_tmdb_filmes:
            dados = api.obter_informacoes_filme_por_id(id)
            dataBase.inserirFilmeDataBase(dados_filme=dados)
            sinopse = dados['sinopse']
            id_filme = dataBase.proximoIdFilme()-1
            sinopse = self.removerCaracteresEspeciais(sinopse)
            sinopse = self.removerStopwords(sinopse)
            #inicializar a chave vazia para dps adicionar
            teste[id_filme] = []
            teste[id_filme].append(sinopse)
            #print(id)


        indice = IndiceInvertido(teste)

        #print(type(indice.invIndex))
        dataBase.inserirIndiceInvertido(indice.invIndex)

    def removerCaracteresEspeciais(self, texto):
        texto_sem_acentuacao = unidecode(texto)
        # Lista de caracteres que serão mantidos
        caracteres_mantidos = string.ascii_letters + string.digits + ' ' + '-'
        # Manter apenas os caracteres desejados
        texto_final = ''.join(char for char in texto_sem_acentuacao if char in caracteres_mantidos)
        return texto_final
    
    def removerStopwords(self, texto):
        # Tokenize o texto em palavras
        palavras = nltk.word_tokenize(texto, language='portuguese')
        # Carregar a lista de stopwords em português
        stopwords_pt = set(stopwords.words('portuguese'))
        # Remover as stopwords
        palavras_sem_stopwords = [palavra for palavra in palavras if palavra.lower() not in stopwords_pt]
        # Recriar o texto sem stopwords
        texto_sem_stopwords = ' '.join(palavras_sem_stopwords)
        return texto_sem_stopwords
    
    def pesquisarFilme(self, string):
        dataBase = ManipularDataBase()
        indice_invertido = dataBase.recuperarIndiceInvertido()
        id_filmes = calcular_tfidf(string, indice_invertido)
        dados = {}
        dados["dados"] = []
        for id in id_filmes:
            filme = dataBase.recuperarFilmePorID(id)
            dados["dados"].append(filme)
        return dados
    
    def adicionarFilme(self, dados):
        dataBase = ManipularDataBase()
        dataBase.inserirFilmeDataBase(dados)
        id_filme = dataBase.proximoIdFilme()
        if(id_filme == None):
            id_filme = 0
        else:
            id_filme -= 1
        sinopse = dados['sinopse']
        sinopse = self.removerCaracteresEspeciais(sinopse)
        sinopse = self.removerStopwords(sinopse)
        teste = {}
        teste[id_filme] = []
        teste[id_filme].append(sinopse)

        indice = IndiceInvertido(teste)
        dataBase.apagarIndiceInvertido()
        confirmacao = dataBase.inserirIndiceInvertido(indice.invIndex)
        return confirmacao

