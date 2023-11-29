document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.querySelector('button');

    searchButton.addEventListener('click', function () {
        const searchQuery = searchInput.value.trim();
        if (searchQuery !== '') {
            // Call the API to search for movies using GET
            searchMovies(searchQuery);
        }
    });
});

function searchMovies(query) {
    const url = `http://localhost:5000/pesquisarFilme?string=${encodeURIComponent(query)}`;

    const requestOptions = {
        headers: {
            'Accept': 'application/json',
        },
    };

    fetch(url, requestOptions)
    .then(response => response.text())
    .then(data => {
        try {
            const jsonData = JSON.parse(data);
            console.log('API Response:', jsonData);
            if (Array.isArray(jsonData)) {
                displayMovies(jsonData);
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
        posterElement.innerHTML = `
            <img src="${movie.poster_path}" alt="${movie.titulo}">
            <p>${movie.titulo}</p>
        `;
        postersContainer.appendChild(posterElement);
    });
}