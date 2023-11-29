const id = 0;
const titulo = document.getElementById('titulo').value;
const generos = document.getElementById('generos').value;
const orcamento = document.getElementById('orcamento').value;
const receita = document.getElementById('receita').value;
const data_lancamento = document.getElementById('data_lancamento').value;
const tempo_duracao = document.getElementById('tempo_duracao').value;
const slogan = document.getElementById('slogan').value;
const popularidade = document.getElementById('popularidade').value;
const total_votos = document.getElementById('total_votos').value;
const media_votos = document.getElementById('media_votos').value;
const poster_path = document.getElementById('poster_path').value;
const sinopse = document.getElementById('sinopse').value;


const movieData = {
    id: 0,
    titulo:titulo,
    generos:generos,
    orcamento: orcamento,
    receita: receita,
    data_lancamento: data_lancamento,
    tempo_duracao: tempo_duracao,
    slogan: slogan,
    popularidade: popularidade,
    total_votos: total_votos,
    media_votos: media_votos,
    poster_path: poster_path,
    sinopse: sinopse
};

fetch('http://localhost:5000/adicionarFilme', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(movieData)
})
.then(response => response.json())
.then(data => console.log('Movie added successfully:', data))
.catch((error) => {
    console.error('Error:', error);
});
