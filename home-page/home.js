document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.querySelector('button');

    searchButton.addEventListener('click', function () {
        const searchQuery = searchInput.value.trim();
        if (searchQuery !== '') {
            // Call the API to search for movies using POST
            searchMovies(searchQuery);
        }
    });
});

function searchMovies(query) {
    const url = `http://localhost:5000/pesquisarFilme/${query}`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': '*/*',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        try {
            console.log('API Response:', data);

            if (Array.isArray(data.dados)) {
                // Os dados estão dentro da propriedade "dados"
                const moviesArray = data.dados;

                // Agora você pode fazer o que quiser com os dados
                displayMovies(moviesArray);
            } else {
                console.error('Error: Response is not an array.');
            }
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function displayMovies(movies) {
    const postersContainer = document.getElementById('posters');
    postersContainer.innerHTML = '';
    movies.forEach(movie => {
        const posterElement = document.createElement('div');
        posterElement.classList.add('poster'); // Adiciona a classe 'poster' ao elemento do pôster
        posterElement.innerHTML = `
            <img src="${movie.poster_path}" alt="${movie.titulo}">
            <p>${movie.titulo}</p>
        `;
        postersContainer.appendChild(posterElement);
    });
}

// Adicione um evento de clique para os pôsteres
document.getElementById('posters').addEventListener('click', function (event) {
    const clickedElement = event.target;

    // Verifica se o clique ocorreu em um elemento com a classe 'poster' ou em seus filhos
    const posterElement = clickedElement.closest('.poster');
    if (posterElement) {
        // Obtém o título do filme a partir do pôster
        const movieTitle = posterElement.querySelector('img').alt;

        // Chama a função para obter os detalhes do filme por título
        getMovieDetailsByTitle(movieTitle);
    }
});

function getMovieDetailsByTitle(title) {
    const url = `http://localhost:5000/pesquisarFilme/${title}`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': '*/*',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        try {
            console.log('Dados recebidos:', data);

            // Exiba os detalhes do filme na janela de detalhes
            displayMovieDetails(data);
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function displayMovieDetails(data) {
    const detailsContainer = document.getElementById('movieDetailsContainer');
    detailsContainer.innerHTML = '';

    // Certifique-se de que 'dados' é um array e tem pelo menos um item
    if (Array.isArray(data.dados) && data.dados.length > 0) {
        const movieDetails = data.dados[0];

        // Criar elementos para exibir os detalhes do filme
        const titleElement = document.createElement('h2');
        titleElement.textContent = movieDetails.titulo;

        const descriptionElement = document.createElement('p');
        descriptionElement.textContent = movieDetails.sinopse;

        // Adicionar elementos ao contêiner de detalhes
        detailsContainer.appendChild(titleElement);
        detailsContainer.appendChild(descriptionElement);

        // Adicionar outras informações
        const releaseDateElement = document.createElement('p');
        releaseDateElement.textContent = `Data de Lançamento: ${movieDetails.data_lancamento}`;
        detailsContainer.appendChild(releaseDateElement);

        const budgetElement = document.createElement('p');
        budgetElement.textContent = `Orçamento: ${movieDetails.orcamento}`;
        detailsContainer.appendChild(budgetElement);

        const voteAverageElement = document.createElement('p');
        voteAverageElement.textContent = `Média de Votos: ${movieDetails.media_votos}`;
        detailsContainer.appendChild(voteAverageElement);

        const genresElement = document.createElement('p');
        genresElement.textContent = `Gêneros: ${movieDetails.generos.join(', ')}`;
        detailsContainer.appendChild(genresElement);

        const popularityElement = document.createElement('p');
        popularityElement.textContent = `Popularidade: ${movieDetails.popularidade}`;
        detailsContainer.appendChild(popularityElement);

        const revenueElement = document.createElement('p');
        revenueElement.textContent = `Receita: ${movieDetails.receita}`;
        detailsContainer.appendChild(revenueElement);

        const sloganElement = document.createElement('p');
        sloganElement.textContent = `Slogan: ${movieDetails.slogan}`;
        detailsContainer.appendChild(sloganElement);

        const durationElement = document.createElement('p');
        durationElement.textContent = `Tempo em minutos: ${movieDetails.tempo_duracao}`;
        detailsContainer.appendChild(durationElement);

        // Adicione mais elementos conforme necessário para outras informações
    } else {
        // Caso não haja dados válidos
        const errorElement = document.createElement('p');
        errorElement.textContent = 'Detalhes do filme não encontrados.';
        detailsContainer.appendChild(errorElement);
    }
}