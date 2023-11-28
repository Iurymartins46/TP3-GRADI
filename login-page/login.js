function checkLogin() {
    // Lógica de verificação de login simples.
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // Aqui você pode adicionar lógica mais sofisticada, como fazer uma solicitação para um servidor para verificar as credenciais.
    // Neste exemplo, vamos assumir que o login é bem-sucedido se ambos os campos não estiverem vazios.

    if (email !== '' && password !== '') {
        // Login bem-sucedido, redirecionar para a página home.
        window.location.href = './home/home-page.html';
    } else {
        alert('Credenciais inválidas. Por favor, tente novamente.');
    }
}