// home.js

const apiKey = '7fdd5a8f';
const apiUrl = `https://www.omdbapi.com/?apikey=${apiKey}`;

// Função para buscar filmes na API
async function searchMovies(searchTerm) {
    try {
        const response = await fetch(`${apiUrl}&s=${searchTerm}`);
        const data = await response.json();

        // Verifica se a resposta foi bem-sucedida
        if (data.Response === 'True') {
            displayMovies(data.Search);
        } else {
            console.error(data.Error);
            displayErrorMessage(data.Error); // Adiciona uma função para exibir mensagens de erro
        }
    } catch (error) {
        console.error('Erro ao buscar filmes:', error);
        displayErrorMessage('Erro ao buscar filmes. Tente novamente mais tarde.'); // Mensagem de erro genérica
    }
}

// Função para exibir os pôsteres dos filmes na página
function displayMovies(movies) {
    const postersContainer = document.getElementById('posters');

    // Limpa o conteúdo atual
    postersContainer.innerHTML = '';

    // Verifica se há filmes encontrados
    if (movies && movies.length > 0) {
        // Itera sobre a lista de filmes
        movies.forEach(movie => {
            const posterElement = document.createElement('div');
            posterElement.classList.add('poster');

            // Adiciona a imagem do pôster
            if (movie.Poster !== 'N/A') {
                const posterImage = document.createElement('img');
                posterImage.src = movie.Poster;
                posterImage.alt = movie.Title;
                posterElement.appendChild(posterImage);
            } else {
                // Caso não tenha pôster, exibe um texto alternativo
                const noPosterText = document.createElement('p');
                noPosterText.textContent = 'Sem pôster disponível';
                posterElement.appendChild(noPosterText);
            }

            // Adiciona o título do filme
            const titleElement = document.createElement('p');
            titleElement.textContent = movie.Title;
            posterElement.appendChild(titleElement);

            // Adiciona o ano de lançamento
            const yearElement = document.createElement('p');
            yearElement.textContent = movie.Year;
            posterElement.appendChild(yearElement);

            // Adiciona o elemento do pôster ao contêiner
            postersContainer.appendChild(posterElement);
        });
    } else {
        displayErrorMessage('Nenhum filme encontrado.'); // Mensagem quando não há resultados
    }
}

// Função para exibir mensagens de erro
function displayErrorMessage(message) {
    const errorElement = document.createElement('p');
    errorElement.textContent = message;
    errorElement.style.color = 'red';
    
    const postersContainer = document.getElementById('posters');
    postersContainer.innerHTML = ''; // Limpa o conteúdo atual
    postersContainer.appendChild(errorElement);
}

// Adiciona um evento de escuta para a tecla Enter na barra de busca
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        const searchTerm = searchInput.value;
        searchMovies(searchTerm);
    }
});

// Chama a função de busca inicial ao carregar a página
searchMovies('avengers'); // Pode ser um termo padrão ou vazio, dependendo de sua preferência

// Função para obter detalhes de um filme por título
async function getMovieDetailsByTitle(movieTitle) {
    try {
        const response = await fetch(`${apiUrl}&t=${encodeURIComponent(movieTitle)}`);
        const data = await response.json();

        // Verifica se a resposta foi bem-sucedida
        if (data.Response === 'True') {
            displayMovieDetails(data);
        } else {
            console.error(data.Error);
            displayErrorMessage(data.Error);
        }
    } catch (error) {
        console.error('Erro ao obter detalhes do filme:', error);
        displayErrorMessage('Erro ao obter detalhes do filme. Tente novamente mais tarde.');
    }
}


// Função para exibir os detalhes do filme clicado
function displayMovieDetails(movie) {
    const postersContainer = document.getElementById('posters');
    const movieDetailsContainer = document.getElementById('movieDetailsContainer');

    // Remove os detalhes anteriores
    while (movieDetailsContainer.firstChild) {
        movieDetailsContainer.removeChild(movieDetailsContainer.firstChild);
    }

    // Crie um elemento div para os detalhes do filme
    const movieDetailsElement = document.createElement('div');
    movieDetailsElement.classList.add('movie-details');

    // Adicione o pôster
    const posterImage = document.createElement('img');
    posterImage.src = movie.Poster;
    posterImage.alt = movie.Title;
    movieDetailsElement.appendChild(posterImage);

    // Adicione o nome, resumo, tempo de duração, data de lançamento e gêneros
    const titleElement = document.createElement('h2');
    titleElement.textContent = movie.Title;
    movieDetailsElement.appendChild(titleElement);

    const plotElement = document.createElement('p');
    plotElement.textContent = movie.Plot;
    movieDetailsElement.appendChild(plotElement);

    const durationElement = document.createElement('p');
    durationElement.textContent = `Duração: ${movie.Runtime}`;
    movieDetailsElement.appendChild(durationElement);

    const releaseDateElement = document.createElement('p');
    releaseDateElement.textContent = `Data de Lançamento: ${movie.Released}`;
    movieDetailsElement.appendChild(releaseDateElement);

    const genresElement = document.createElement('p');
    genresElement.textContent = `Gêneros: ${movie.Genre}`;
    movieDetailsElement.appendChild(genresElement);

    // Adicione o elemento de detalhes ao contêiner
    movieDetailsContainer.appendChild(movieDetailsElement);
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
