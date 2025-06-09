// login.js

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const errorMsg = document.getElementById('error-msg');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = form.username.value;
    const password = form.password.value;

    try {
      const response = await fetch('http://127.0.0.1:8000/api/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        // ✅ Guardamos el token
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);

        // ✅ Redirigimos al dashboard
        window.location.href = 'dashboard.html';
      } else {
        // ❌ Error de login
        errorMsg.classList.remove('hidden');
      }

    } catch (err) {
      console.error('Error al iniciar sesión:', err);
      errorMsg.textContent = 'Error al conectar con el servidor.';
      errorMsg.classList.remove('hidden');
    }
  });
});
