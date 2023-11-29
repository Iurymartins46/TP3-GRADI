window.onload = function() {
    var userName = localStorage.getItem('userName');
    if (userName) {
        document.getElementById('user-name').textContent = 'Olá, ' + userName + '!';
    } else {
        // Exibir mensagem de erro e solicitar que o usuário tente novamente
        alert('Erro ao obter informações do usuário. Por favor, tente novamente.');
    }
};

function logout() {
    // Remover o nome do usuário do localStorage
    localStorage.removeItem('userName');

    // Redirecionar para a página de login
    window.location.href = '../login-page/login.html';
}