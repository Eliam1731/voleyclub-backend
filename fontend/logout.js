// logout.js
document.addEventListener('DOMContentLoaded', () => {
  const logoutBtn = document.getElementById('logout-btn');

  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      // Elimina los tokens
      localStorage.removeItem('access');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh');
      localStorage.removeItem('refresh_token');

      // Limpia historial de navegación y redirige
      window.location.replace('login.html'); // Reemplaza sin dejar rastro en historial

      // Previene volver con "atrás" o "adelante"
      history.pushState(null, null, 'login.html');
      window.addEventListener('popstate', () => {
        history.pushState(null, null, 'login.html');
      });
    });
  }
});
