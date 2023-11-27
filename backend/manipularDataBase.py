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
        
    
    def inserirIndice(self,arraySinopses) -> bool:
            
            nome_data_base = "TP3-GRADI"
            xml_doc_name = "indiceInvertido.xml"
            index = IndiceInvertido(arraySinopses)
            print(index.invIndex)

            sentencas_entries = []

            for word, positions in index.invIndex.items():
                consolidated_positions = ', '.join([f"[{pos[0]}, {pos[1]}]" for pos in positions])
                word_entry = {"@palavra": word, "#text": consolidated_positions}
                sentencas_entries.append(word_entry)

            # Adiciona um elemento "sentencas" que envolve todas as entradas
            xml_dict = {"indiceInvertido": {"sentencas": sentencas_entries}}

            # Abre o arquivo XML para escrita
            with open("person.xml", "w") as xml_file:
                xmltodict.unparse(xml_dict, output=xml_file, pretty=True)

            with open("person.xml", "r") as xml_file:
                xml_index = xml_file.read()

            xml_index = xml_index.replace('<?xml version="1.0" encoding="utf-8"?>', '')

        
            try:
                session = self.conectarDataBase()

                # Verificar se o nó indice já existe no documento
                check_query = session.query(f'''
                    let $db := "{nome_data_base}"
                    let $doc := db:open($db, "{xml_doc_name}")
                    return exists($doc//indice)
                ''')

                if not check_query.execute():
                    # Se o nó indice não existir, crie-o
                    create_query = session.query(f'''
                        let $db := "{nome_data_base}"
                        let $doc := db:open($db, "{xml_doc_name}")
                        return
                            insert node <indice/> as last into $doc
                    ''')
                    create_query.execute()

                    # Agora, execute a consulta de inserção
                    insert_query = session.query(f'''
                        let $db := "{nome_data_base}"
                        let $doc := db:open($db, "{xml_doc_name}")
                        let $novoIndice := {xml_file}
                        return
                            insert node $novoIndice as last into $doc//indice
                    ''')
                    result = insert_query.execute()

                    xml_file.close()
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

    
            
            self.inserirIndice(arraySinopses)
        
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
        
        


   

            

