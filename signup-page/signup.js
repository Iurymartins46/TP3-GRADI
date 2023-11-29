document.getElementById('voltar').addEventListener('click', function() {
    window.location.href = '../login-page/login.html';
});

document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signup-form');

    signupForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Assuming you have a function named createUser in your backend API
        createUser(name, email, password);
    });

    // Function to create a new user
    function createUser(name, email, password) {
        const url = 'http://localhost:5000/criarNovoUsuario'; // Update the URL with your actual endpoint
        const userData = {
            name: name,
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
            console.log('Response:', data);
            // Handle the response data as needed (e.g., show success message or redirect)
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});