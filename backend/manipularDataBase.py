from BaseXClient import BaseXClient
import xml.etree.ElementTree as ET
from xml.dom import minidom

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
    
    def criarDataBase(self, nome_data_base) -> bool:
        nome_documento_dados = "dados.xml"
        nome_documento_indices = "indices.xml"

        # Criar a raiz do documento
        raiz_documento_dados = ET.Element("filmes")
        # Criar uma representação de string com formatação
        xml_documento_dados = ET.tostring(raiz_documento_dados, encoding="unicode")
        xml_documento_dados = minidom.parseString(xml_documento_dados)
        xml_documento_dados = xml_documento_dados.toprettyxml(indent="    ")  # Especifica a quantidade de espaços para a indentação

        # Criar a raiz do documento
        raiz_documento_indices = ET.Element("indices")
        # Criar uma representação de string com formatação
        xml_documento_indices = ET.tostring(raiz_documento_indices, encoding="unicode")
        xml_documento_indices = minidom.parseString(xml_documento_indices)
        xml_documento_indices = xml_documento_indices.toprettyxml(indent="    ")  # Especifica a quantidade de espaços para a indentação


        try:
            session = self.conectarDataBase()
            if self.verificarExisteDataBase(session, nome_data_base):
                self.fecharDataBase(session)
                return True
            else:
                session.execute(f"CREATE DB {nome_data_base}")
                session.execute(f"OPEN {nome_data_base}")
                session.add(nome_documento_dados, xml_documento_dados)
                session.add(nome_documento_indices, xml_documento_indices)
                self.fecharDataBase(session)
                return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
        