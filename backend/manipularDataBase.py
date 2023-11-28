from BaseXClient import BaseXClient
import xml.etree.ElementTree as ET
import sys
sys.path.append('backend')

from indiceInvertido import IndiceInvertido


import os
from dotenv import load_dotenv

class ManipularDataBase:

    def conectarDataBase(self):
        load_dotenv()
        try:
            host = os.getenv("HOST_DB")  # Endereço do servidor BaseX
            port = int(os.getenv("PORT_DB"))  # Porta padrão do servidor BaseX
            user = os.getenv("USER_DB")     # Nome de usuário (se necessário)
            password = os.getenv("SENHA_DB")  # Senha (se necessário)
            session = BaseXClient.Session(host, port, user, password)
            return session
        except Exception as erro:
            print(f"Erro ao se conectar ao banco de dados")
            print(f"Tipo de excecao: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None
    
    def fecharDataBase(self, session):
        session.close()

    def verificarExisteDataBase(self, session, nome_data_base) -> bool:
        databases = session.execute("XQUERY db:list()")
        if nome_data_base in databases:
            return True
        else:
            return False
    
    def criarDataBase(self) -> bool:
        nome_data_base = "TP3-GRADI"
        nome_documento_dados = "dados.xml"
        nome_documento_indices = "indices.xml"
        nome_documento_usuarios = "usuarios.xml"

        xml_dados = """<filmes></filmes>"""
        xml_indices = """<indices></indices>"""
        xml_usuarios = """<usuarios></usuarios>"""

        try:
            session = self.conectarDataBase()
            if self.verificarExisteDataBase(session, nome_data_base):
                self.fecharDataBase(session)
                return True
            else:
                session.execute(f"CREATE DB {nome_data_base}")
                session.execute(f"OPEN {nome_data_base}")
                session.add(nome_documento_dados, xml_dados)
                session.add(nome_documento_indices, xml_indices)
                session.add(nome_documento_usuarios, xml_usuarios)
                self.fecharDataBase(session)
                return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
        
    def inserirIndiceInvertido(self,indiceInvertido) -> bool:
        nome_data_base = "TP3-GRADI"
        nome_documento_indices = "indices.xml"
        try:
            session = self.conectarDataBase()
            for key, value in indiceInvertido.items():
                xml_index = f"""<sentenca palavra = '{key}'>{value}</sentenca>"""
                insert_query = session.query(f'''
                    let $db := "{nome_data_base}"
                    let $doc := db:open($db, "{nome_documento_indices}")
                    let $novoIndice := {xml_index}
                    return
                        insert node $novoIndice as last into $doc//indices
                ''')
                result = insert_query.execute()

            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
        
    def apagarIndiceInvertido(self):
        nome_data_base = "TP3-GRADI"
        nome_documento_indices = "indices.xml"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{nome_documento_indices}")
                return
                    delete nodes $doc//indices/*
            ''')
            result = query.execute()
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
        
    def recuperarIndiceInvertido(self):
        nome_data_base = "TP3-GRADI"
        nome_documento_indices = "indices.xml"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{nome_documento_indices}")
                for $sentencas in $doc//indices/sentenca
                return $sentencas
            ''')
            result = query.execute()
            self.fecharDataBase(session)

            root = ET.fromstring("<root>" + result + "</root>")
            sentencas = root.findall('sentenca')

            # Iterar sobre os elementos <sentenca> e extrair  conteúdo
            dados = {}
            for sentenca in sentencas:
                palavra = sentenca.get('palavra')
                conteudo = sentenca.text
                dados[f"{palavra}"] = eval(conteudo)
            return dados
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None

    def inserirFilmeDataBase(self, dados_filme) -> bool:
        nome_data_base = "TP3-GRADI"
        nome_documento_dados = "dados.xml"
        id_filme = self.proximoIdFilme()
        xml_filme = f"""
        <filme id='{id_filme}'>
            <id_tmdb>{dados_filme["id"]}</id_tmdb>
            <titulo>{dados_filme["titulo"]}</titulo>
            <generos>{''.join([f'<genero id="{genero["id"]}">{genero["name"]}</genero>' for genero in dados_filme["generos"]])}</generos>
            <orcamento>{dados_filme["orcamento"]}</orcamento>
            <receita>{dados_filme["receita"]}</receita>
            <data_lancamento>{dados_filme["data_lancamento"]}</data_lancamento>
            <tempo_duracao>{dados_filme["tempo_duracao"]}</tempo_duracao>
            <slogan>{dados_filme["slogan"]}</slogan>
            <popularidade>{dados_filme["popularidade"]}</popularidade>
            <total_votos>{dados_filme["total_votos"]}</total_votos>
            <media_votos>{dados_filme["media_votos"]}</media_votos>
            <poster_path>{dados_filme["poster_path"]}</poster_path>
            <sinopse>{dados_filme["sinopse"]}</sinopse>
        </filme>
        """ 

        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{nome_documento_dados}")
                let $novoFilme := {xml_filme}
                return
                    insert node $novoFilme as last into $doc//filmes
            ''')
            result = query.execute()
        
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False

    def proximoIdFilme(self):
        nome_data_base = "TP3-GRADI"
        nome_documento_dados = "dados.xml"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{nome_documento_dados}")
                let $filmes := $doc//filmes/filme
                let $ultimoFilme := $filmes[last()]
                return xs:integer($ultimoFilme/@id)
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            last_user_id = int(result) if result else -1
            return last_user_id + 1
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return None

    def recuperarFilmePorID(self, id):
        nome_data_base = "TP3-GRADI"
        nome_documento_dados = "dados.xml"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{nome_documento_dados}")
                for $filme in $doc//filmes/filme[@id = {id}]
                return $filme
            ''')
            result = query.execute()
            self.fecharDataBase(session)

            # Iterar sobre os elementos <sentenca> e extrair  conteúdo
            dados = {}
            root = ET.fromstring(result)
            for child in root:
                if len(child) > 0:
                    # Se o elemento tem filhos, crie um dicionário para ele
                    dados[child.tag] = []
                    for subchild in child:
                        dados[child.tag].append(subchild.text)
                else:
                    # Se o elemento não tem filhos, apenas adicione ao dicionário
                    dados[child.tag] = child.text
            
            return dados

        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None
    
    def criarUsuario(self, email, senha):
        nome_documento_usuarios = "usuarios.xml"
        nome_data_base = "TP3-GRADI"
        try:
            id_usuario = self.proximoIdUsuario()
            xml_usuario = f"""
            <usuario id="{id_usuario}">
                <email>{email}</email>
                <senha>{senha}</senha>
            </usuario>"""
            session = self.conectarDataBase()
            query = session.query(f'''
            let $db := "{nome_data_base}"
            let $doc := db:open($db, "{nome_documento_usuarios}")
            let $novoUsuario := {xml_usuario}
            return
                insert node $novoUsuario as last into $doc//usuarios
        ''')
            result = query.execute()
            self.fecharDataBase(session)
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False

    def proximoIdUsuario(self):
        nome_documento_usuarios = "usuarios.xml"
        nome_data_base = "TP3-GRADI"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{nome_documento_usuarios}")
                let $usuarios := $doc//usuarios/usuario
                let $ultimoUsuario := $usuarios[last()]
                return xs:integer($ultimoUsuario/@id)
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            last_user_id = int(result) if result else -1
            return last_user_id + 1
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return None

    def pesquisarUsuarioPorSenhaEmail(self, email, senha):
        nome_documento_usuarios = "usuarios.xml"
        nome_data_base = "TP3-GRADI"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{nome_documento_usuarios}")
                let $usuario := $doc//usuarios/usuario[./email = "{email}" and ./senha = "{senha}"]
                return xs:integer($usuario/@id)
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            return result
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None
