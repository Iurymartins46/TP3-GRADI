document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    if (email === 'teste@gmail.com' && password === '123456') {
        window.location.href = '../home-page/home.html';
    } else if (email === 'admin@gmail.com' && password === '123456') {
        window.location.href = '../admin-page/admin.html';
    } else {
        alert('Usuário ou senha inválidos.');
    }
});

document.getElementById('cadastrar').addEventListener('click', function() {
    window.location.href = '../signup-page/signup.html';
});