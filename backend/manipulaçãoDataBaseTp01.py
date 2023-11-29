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

    def verificarExisteDataBase(self, session, nome_data_base):
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
        
    def criarUsuario(self, email, senha):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        id_usuario = self.proximo_id_usuario()
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
            let $db := "{nome_data_base}"
            let $doc := db:open($db, "{xml_doc_name}")
            let $novoUsuario := <usuario id="{id_usuario}">
                <email>{email}</email>
                <senha>{senha}</senha>
            </usuario>
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

    def criarDiario(self, titulo, data, conteudo, tag, usuario_id):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        diario_id = self.proximo_id_diario(usuario_id)
        diario = f"""
            <diario id="{diario_id}">
                <titulo>{titulo}</titulo>
                <data>{data}</data>
                <conteudo>{conteudo}</conteudo>
                <tag>{tag}</tag>
            </diario>
            """
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
            let $db := "{nome_data_base}"
            let $doc := db:open($db, "{xml_doc_name}")
            let $novoDiario := {diario}
            let $usuario := $doc//usuarios/usuario[@id="{usuario_id}"]
            let $diarios := $usuario/diarios
            return
                if (empty($diarios)) then
                    insert node element diarios {{$novoDiario}} as last into $usuario
                else
                    insert node $novoDiario as last into $diarios
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False

    def atualizarTitulo(self, usuario_id, diario_id, novo_titulo):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                let $usuario := $doc//usuarios/usuario[@id="{usuario_id}"]
                let $diario := $usuario/diarios/diario[@id="{diario_id}"]
                return
                    replace value of node $diario/titulo with "{novo_titulo}"
            ''')    
            result = query.execute()
            self.fecharDataBase(session)
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False

    def atualizarConteudo(self, usuario_id, diario_id, novo_conteudo):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                let $usuario := $doc//usuarios/usuario[@id="{usuario_id}"]
                let $diario := $usuario/diarios/diario[@id="{diario_id}"]
                return
                    replace value of node $diario/conteudo with "{novo_conteudo}"
            ''')    
            result = query.execute()
            self.fecharDataBase(session)
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
    
    def atualizarTag(self, usuario_id, diario_id, nova_tag):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                let $usuario := $doc//usuarios/usuario[@id="{usuario_id}"]
                let $diario := $usuario/diarios/diario[@id="{diario_id}"]
                return
                    replace value of node $diario/tag with "{nova_tag}"
            ''')    
            result = query.execute()
            self.fecharDataBase(session)
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
        
    def apagarDiario(self, usuario_id, diario_id):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                let $usuario := $doc//usuarios/usuario[@id="{usuario_id}"]
                let $diario := $usuario/diarios/diario[@id="{diario_id}"]
                return
                    delete node $diario
            ''')    
            result = query.execute()
            self.fecharDataBase(session)
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False

    def apagarUsuario(self, usuario_id):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                let $usuario := $doc//usuarios/usuario[@id="{usuario_id}"]
                return
                    delete node $usuario
            ''')    
            result = query.execute()
            self.fecharDataBase(session)
            return True
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            self.fecharDataBase(session)
            return False
         
    def proximo_id_usuario(self):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
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

    def proximo_id_diario(self, usuario_id):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                let $usuarios := $doc//usuarios/usuario
                let $ultimoDiario := $usuarios[@id = {usuario_id}]/diarios/diario[last()]
                return xs:integer($ultimoDiario/@id)
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
        
    def padronizaRetornoDiario(self, result):
        if result:
            #xml_elements = result.strip().split("\n")
            diarios = []
            xml_elements = []
            root = ET.fromstring("<root>" + result + "</root>")
            for diario_elem in root:
                if diario_elem.tag == 'diario':
                    xml_elements.append(ET.tostring(diario_elem, encoding='utf-8').decode('utf-8'))
            
            for xml_element in xml_elements:
                diario = dict()
                root = ET.fromstring(xml_element)
                diario_id = int(root.get("id"))
                titulo = root.find("titulo").text
                data = root.find("data").text
                conteudo = root.find("conteudo").text
                tag_diario = root.find("tag").text

                diario["id"] = diario_id
                diario["titulo"] = titulo
                diario["data"] = data
                diario["conteudo"] = conteudo
                diario["tag"] = tag_diario
                diarios.append(diario)
            return diarios
        else:
            return None

    def listarDiariosPorTag(self, usuario_id, tag):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                for $diario in $doc//usuarios/usuario[@id = {usuario_id}]/diarios/diario
                where $diario/tag = "{tag}"
                return $diario
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            return self.padronizaRetornoDiario(result)
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None

    def listarDiariosPorTitulo(self, usuario_id, titulo):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                for $diario in $doc//usuarios/usuario[@id = {usuario_id}]/diarios/diario
                where contains($diario/titulo, "{titulo}")
                return $diario
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            return self.padronizaRetornoDiario(result)
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None

    def listarDiariosPorConteudo(self, usuario_id, conteudo):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                for $diario in $doc//usuarios/usuario[@id = {usuario_id}]/diarios/diario
                where contains($diario/conteudo, "{conteudo}")
                return $diario
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            return self.padronizaRetornoDiario(result)
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None
        
    def listarDiariosPorData(self, usuario_id, data):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                for $diario in $doc//usuarios/usuario[@id = {usuario_id}]/diarios/diario
                where $diario/data = "{data}"
                return $diario
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            return self.padronizaRetornoDiario(result)
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None
        
    def listarTodosDiarios(self, usuario_id):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
                for $diario in $doc//usuarios/usuario[@id = {usuario_id}]/diarios/diario
                return $diario
            ''')
            result = query.execute()
            self.fecharDataBase(session)
            return self.padronizaRetornoDiario(result)
        except Exception as erro:
            print(f"Tipo de exceção: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None

    #return usuario_id, caso tenha esse usuario cadastrado
    def pesquisarUsuarioPorSenhaEmail(self, email, senha):
        xml_doc_name = "diario.xml"
        nome_data_base = "Diario"
        try:
            session = self.conectarDataBase()
            query = session.query(f'''
                let $db := "{nome_data_base}"
                let $doc := db:open($db, "{xml_doc_name}")
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
        