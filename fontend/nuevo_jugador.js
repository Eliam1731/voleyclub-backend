// Mostrar nombre de archivos seleccionados
const archivoFoto = document.getElementById('foto');
const archivoCurp = document.getElementById('curp');
const archivoActa = document.getElementById('acta_nacimiento');

archivoFoto?.addEventListener('change', () => {
  const archivo = archivoFoto.files[0];
  document.getElementById('nombre-foto').textContent = archivo ? archivo.name : 'Seleccionar archivo';
});

archivoCurp?.addEventListener('change', () => {
  const archivo = archivoCurp.files[0];
  document.getElementById('nombre-curp').textContent = archivo ? archivo.name : 'Seleccionar archivo';
});

archivoActa?.addEventListener('change', () => {
  const archivo = archivoActa.files[0];
  document.getElementById('nombre-acta').textContent = archivo ? archivo.name : 'Seleccionar archivo';
});

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form-jugador');
  const token = localStorage.getItem('access') || localStorage.getItem('access_token');

  // 👉 Cargar entrenadores
  fetch('http://127.0.0.1:8000/api/entrenadores/', {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(res => res.json())
    .then(entrenadores => {
      const select = document.getElementById('entrenador');
      entrenadores.forEach(entrenador => {
        const option = document.createElement('option');
        option.value = entrenador.id;
        option.textContent = entrenador.nombre_completo;
        select.appendChild(option);
      });
    })
    .catch(err => {
      console.error('Error al cargar entrenadores:', err);
    });

  // 👉 Evento submit
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/jugadores/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) throw new Error('No se pudo guardar el jugador');

      alert('Jugador guardado exitosamente');
      window.location.href = 'jugadores.html';

    } catch (error) {
      console.error('Error al guardar jugador:', error);
      alert('Error al guardar jugador.');
    }
  });
});
