import requests

api_key = '37536199a87edd04b278fadfa0e140d0'
base_url = 'https://api.themoviedb.org/3/'
language = 'pt-BR'

class ManipularAPI:
     
    def obter_id_filme_por_nome(self, nome_filme):
        try:
            endpoint_busca = 'search/movie'
            params_busca = {'api_key': api_key, 'query': nome_filme, 'language': language,
                             'media_type': 'movie', "sort_by" : 'popularity.desc', 'country': 'BR'}
            response_busca = requests.get(base_url + endpoint_busca, params=params_busca)
            if response_busca.status_code == 200:
                resultados_busca = response_busca.json()['results']
                filme_id = []
                for resultado in resultados_busca:
                    """
                    id_documentario : 99
                    Uma verificação para não retornar documentarios, e para o filme ter sido
                    avaliado por mais de 99 pessoas
                    """
                    if 99 not in resultado['genre_ids'] and resultado['vote_count'] > 99:
                        filme_id.append(resultado['id'])
                return filme_id
            return None
        except Exception as erro:
            print(f"Erro ao se conectar ao banco de dados")
            print(f"Tipo de excecao: {type(erro).__name__}")
            print(f"Mensagem de erro: {str(erro)}")
            return None

    def obter_informacoes_filme_por_id(self, id_filme):
        try:
            endpoint_filme = f'movie/{id_filme}'
            params_filme = {'api_key': api_key, 'language': language}
            response_filme = requests.get(base_url + endpoint_filme, params=params_filme)
            if response_filme.status_code == 200:
                informacoes_filme = response_filme.json()
                """for chave, valor in informacoes_filme.items():
                    print(f"Chave: {chave}, Valor: {valor}")"""
                dados_filme = dict()
                dados_filme["id"] = informacoes_filme["id"]
                dados_filme["titulo"] = informacoes_filme["title"]
                dados_filme["generos"] = informacoes_filme["genres"]
                #dados_filme["genero"] = [item['name'] for item in informacoes_filme["genres"]]
                dados_filme["orcamento"] = informacoes_filme["budget"]
                dados_filme["receita"] = informacoes_filme["revenue"]
                dados_filme["data_lancamento"] = informacoes_filme["release_date"]
                dados_filme["tempo_duracao"] = informacoes_filme["runtime"]
                dados_filme["slogan"] = informacoes_filme["tagline"]
                dados_filme["popularidade"] = informacoes_filme["popularity"]
                dados_filme["total_votos"] = informacoes_filme["vote_count"]
                dados_filme["media_votos"] = informacoes_filme["vote_average"]
                dados_filme["sinopse"] = informacoes_filme["overview"]
                base_imagem_url = 'https://image.tmdb.org/t/p/'
                tamanho_poster = 'w300'  # Pode ser ajustado conforme necessário
                url_completo_poster = base_imagem_url + tamanho_poster + informacoes_filme["poster_path"]
                dados_filme["poster_path"] = url_completo_poster
                return dados_filme

            return None

        except Exception as erro:
                print(f"Erro ao se conectar ao banco de dados")
                print(f"Tipo de excecao: {type(erro).__name__}")
                print(f"Mensagem de erro: {str(erro)}")
                return None
