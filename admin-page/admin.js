document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(event.target);
    var data = Object.fromEntries(formData.entries());

    // Faça o que você precisar para salvar as informações no servidor
    console.log(data);
});