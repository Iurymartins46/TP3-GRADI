import axios from 'axios';

export class DiarioServiceService {

  private apiUrl= 'http://127.0.0.1:5000';

  async criarNovoUsuario(email: string, senha: string) {
    
    const body = {
      email: email,
      senha: senha,
    };
    
    const response = await axios.post(`${this.apiUrl}/criarNovoUsuario`, body);

    //alert(response.data);

    return response.data;
  }

  async realizarLogin(email: string, senha: string) {

    const body = {
      email: email,
      senha: senha,
    };

    try {
      const response = await axios.post(`${this.apiUrl}/realizarLogin`, body);
      //alert(response.data);
      return response.data;
      
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      throw error;
    }

    //alert(response.data);

    //return response.data;

  }

  async pesquisarFilme(string: string) {

    const body = {
        string:string
    };

    try {
      const response = await axios.post(`${this.apiUrl}/pesquisarFilme`, body);
      //alert(response.data);
      return response.data;
      
    } catch (error) {
      console.error('Erro ao pesquisar por Filme:', error);
      throw error;
    }

    //alert(response.data);

    //return response.data;

  }

  async adicionarFilme(string: string) {

    const body = {
        string:string
    };

    try {
      const response = await axios.post(`${this.apiUrl}/pesquisarFilme`, body);
      //alert(response.data);
      return response.data;
      
    } catch (error) {
      console.error('Erro ao pesquisar por Filme:', error);
      throw error;
    }

    //alert(response.data);

    //return response.data;

  }

/*  async listarDiarios(usuarioId: string){
    const body = {
      usuario_id: usuarioId
    };

    try {
      const response = await axios.get(`${this.apiUrl}/listarTodosDiarios`);
      return response.data;
    } catch (error) {
      console.error('Erro ao listar diários:', error);
      throw error;
    }
  }

  

  
  async criarDiario(titulo: string, data: string, conteudo: string, tag: string, usuario_id: string) {
    const body = {
      titulo,
      data,
      conteudo,
      tag,
      usuario_id
    };
    try {
      const response = await axios.post(`${this.apiUrl}/criarDiario`, body);
      return response.data;
    } catch (error) {
      console.error('Erro ao criar diário:', error);
      throw error;
    }
  }


  async listarTodosDiarios(usuario_id: string) {
    const body = {
      usuario_id: usuario_id
    };
    console.log("user_body:", body);
    try {
      console.log("try");
      console.log(body.usuario_id);
      const response = await axios.get(`${this.apiUrl}/listarTodosDiarios?usuario_id=${body.usuario_id}`);
      console.log(response.data);
      console.log("passou aqui");
      return response.data;
    } catch (error) {
      console.error('Erro ao listar todos os diários:', error);
      throw error;
    }
  }

*/
}