document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const url = 'http://localhost:5000/realizarLogin';
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const userData = {
        email: email,
        senha: password
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.confirmacao) {
            // Login bem-sucedido, redirecione para a página de administrador
            if (email === 'admin@gmail.com' && password === 'admin') {
                window.location.href = '../admin-page/admin.html';
            } else {
                // Trate aqui o redirecionamento para a página do usuário normal
                window.location.href = '../home-page/home.html';
                alert('Login bem-sucedido! Redirecionar para a página do usuário...');
            }
        } else {
            // Credenciais inválidas
            alert('Usuário ou senha inválidos.');
        }
    })
    .catch(error => {
        console.error('Erro ao realizar login:', error);
    });
});

document.getElementById('cadastrar').addEventListener('click', function() {
    window.location.href = '../signup-page/signup.html';
});