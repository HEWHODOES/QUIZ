
function showRegister() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
    document.getElementById('message').textContent = "";
}

function showLogin() {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('message').textContent = "";    
}

async function register() {
    const username = document.getElementById('register-username').value;

    if (!username) {
        document.getElementById('message').textContent = "Bitte Usernamen eingeben!";
        return
    }

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({username: username})
    });

    const data = await response.json();
    
    if (data.success) {
        window.location.href = '/';
    } else {
        document.getElementById('message').textContent = data.error;
    }
}

async function login() {
    const username = document.getElementById('login-username').value;
    
    if (!username) {
        document.getElementById('message').textContent = 'Bitte Username eingeben!';
        return;
    }
    
    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username })
    });
    
    const data = await response.json();
    
    if (data.success) {
        window.location.href = '/';
    } else {
        document.getElementById('message').textContent = data.error;
    }
}

async function logout() {
    await fetch('/logout', { method: 'POST' });
    window.location.reload();
}