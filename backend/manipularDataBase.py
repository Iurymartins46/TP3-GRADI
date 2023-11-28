from BaseXClient import BaseXClient
import xml.etree.ElementTree as ET
from xml.dom import minidom
import xmltodict
import sys
sys.path.append('backend')

from indiceInvertido import IndiceInvertido


import os
from dotenv import load_dotenv


arraySinopses = []

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

        xml_dados = """<filmes></filmes>"""
        xml_indices = """<indices></indices>"""

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
                self.fecharDataBase(session)
                return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
        
    
    def inserirIndice(self,indiceInvertido) -> bool:
            nome_data_base = "TP3-GRADI"
            xml_doc_name = "indices.xml"
            try:
                session = self.conectarDataBase()
                for k, v in indiceInvertido.items():
                    xml_index = f"""<sentenca palavra = '{k}'>{v}</sentenca>"""
                    insert_query = session.query(f'''
                        let $db := "{nome_data_base}"
                        let $doc := db:open($db, "{xml_doc_name}")
                        let $novoIndice := {xml_index}
                        return
                            insert node $novoIndice as last into $doc//indices
                    ''')
                    print(xml_index)
                    result = insert_query.execute()

                return True
            except Exception as erro:
                print(f"Tipo de exceção: {type(erro).__name__}")
                print(f"Mensagem de erro: {str(erro)}")
                self.fecharDataBase(session)
                return False

    
    def inserirFilmeDataBase(self, dados_filme) -> bool:
        nome_data_base = "TP3-GRADI"
        xml_doc_name = "dados.xml"
        xml_filme = f"""
        <filme id='{dados_filme["id"]}'>
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
        arraySinopses.append(dados_filme["sinopse"])

        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
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
        
        


   

            

