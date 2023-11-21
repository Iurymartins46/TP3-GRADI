document.addEventListener('DOMContentLoaded', function () {
    // Função para fazer a requisição à API e exibir os filmes
    function fetchMovies() {
        const apiKey = '7fdd5a8f'; // Substitua pela sua chave da API OMDb
        const apiUrl = `https://www.omdbapi.com/?s=avengers&apikey=${apiKey}`; // Exemplo: Filmes dos Vingadores

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => displayMovies(data.Search))
            .catch(error => console.error('Erro ao buscar filmes:', error));
    }

    // Função para exibir a lista de filmes
    function displayMovies(movies) {
        const moviesList = document.getElementById('movies-list');
    
        moviesList.innerHTML = '';
    
        if (movies && movies.length > 0) {
            movies.forEach(movie => {
                const poster = movie.Poster === 'N/A' ? 'sem-imagem.jpg' : movie.Poster;
                const movieElement = document.createElement('div');
                movieElement.classList.add('movie');
                movieElement.innerHTML = `
                    <img src="${poster}" alt="${movie.Title}" data-imdb-id="${movie.imdbID}">
                    <p>${movie.Title}</p>
                `;
                moviesList.appendChild(movieElement);
            });
    
            // Adiciona um evento de clique para cada pôster
            const posters = document.querySelectorAll('.movie img');
            posters.forEach(poster => {
                poster.addEventListener('click', () => {
                    const imdbID = poster.getAttribute('data-imdb-id');
                    fetchMovieDetails(imdbID);
                });
            });
        } else {
            moviesList.innerHTML = 'Nenhum filme encontrado.';
        }
    }

    // Função para buscar detalhes de um filme específico
    function fetchMovieDetails(imdbID) {
        const apiKey = 'sua-api-key';
        const apiUrl = `http://www.omdbapi.com/?i=${imdbID}&apikey=${apiKey}`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => displayMovieDetails(data))
            .catch(error => console.error('Erro ao buscar detalhes do filme:', error));
    }

    // Função para exibir os detalhes do filme
    function displayMovieDetails(movieDetails) {
        const movieDetailsContainer = document.getElementById('movie-details');
        movieDetailsContainer.innerHTML = `
            <h2>${movieDetails.Title}</h2>
            <p><strong>Duração:</strong> ${movieDetails.Runtime}</p>
            <p><strong>Sinopse:</strong> ${movieDetails.Plot}</p>
            <!-- Adicione mais detalhes conforme necessário -->
        `;
        movieDetailsContainer.classList.remove('hidden');
    }

    // Inicia a aplicação
    fetchMovies();
});
