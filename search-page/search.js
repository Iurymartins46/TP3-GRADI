document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var searchOption = document.getElementById('search-option').value;
    var searchInput = document.getElementById('search-input').value;

    // Realize a pesquisa aqui e obtenha os resultados
    // Você pode usar o Fetch API, XMLHttpRequest ou qualquer outra biblioteca para fazer a chamada à API
    // Aqui está um exemplo de como você pode obter os resultados, assumindo que a API retorna uma lista de objetos de filme
    var results = [
        {title: 'Filme 1', synopsis: 'Sinopse do Filme 1'},
        {title: 'Filme 2', synopsis: 'Sinopse do Filme 2'},
        // ...
    ];

    // Filtre os resultados com base na opção de pesquisa selecionada e no texto de pesquisa inserido
    var filteredResults = results.filter(function(result) {
        return result[searchOption].toLowerCase().includes(searchInput.toLowerCase());
    });

    // Exiba os resultados na div 'search-results'
    var searchResults = document.getElementById('search-results');
    searchResults.innerHTML = '';
    filteredResults.forEach(function(result) {
        var resultElement = document.createElement('div');
        resultElement.textContent = result.title + ' - ' + result.synopsis;
        searchResults.appendChild(resultElement);
    });
});