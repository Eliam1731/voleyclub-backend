document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem('access');

  // 🔐 Si no hay token, manda al login
  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  try {
    // 🔄 Petición con el token en la cabecera
    const response = await fetch('http://127.0.0.1:8000/api/yo/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      console.warn("Token no válido o expirado");
      window.location.href = 'login.html';
      return;
    }

    const data = await response.json();

    // 👤 Llena los datos del usuario
    document.getElementById('nombre-usuario').textContent = data.nombre_completo || data.username;

    const rolCapitalizado = data.rol.charAt(0).toUpperCase() + data.rol.slice(1);
    document.getElementById('rol-usuario').textContent = `${rolCapitalizado} del Club`;

    const fecha = new Date().toLocaleString('es-MX', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
    document.getElementById('ultimo-acceso').textContent = `Último acceso: ${fecha}`;
    document.getElementById('correo-usuario').textContent = `Correo: ${data.email || 'No disponible'}`;

    // 🖼️ Imagen si está definida
    if (data.foto) {
      document.getElementById('foto-usuario').src = `http://127.0.0.1:8000${data.foto}`;
    }

  } catch (err) {
    console.error("Error al obtener usuario:", err);
    window.location.href = 'login.html';
  }
});
