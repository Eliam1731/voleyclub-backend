document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem('access') || localStorage.getItem('access_token');

  if (!token) return (window.location.href = 'login.html');

  try {
    const response = await fetch('http://127.0.0.1:8000/api/jugadores/', {
      headers: {
        Authorization: `Bearer ${token}`,
      }
    });

    if (!response.ok) throw new Error('No se pudo obtener la lista de jugadores');

    const jugadores = await response.json();
    mostrarJugadores(jugadores);
    agregarEventosVer(jugadores);

  } catch (error) {
    console.error('Error al cargar jugadores:', error);
    alert('Hubo un error al cargar los jugadores.');
  }

  document.getElementById('buscar-input').addEventListener('input', (e) => {
    const texto = e.target.value.toLowerCase();
    const filas = document.querySelectorAll('#jugadores-tbody tr');

    filas.forEach(fila => {
      const nombre = fila.children[0].textContent.toLowerCase();
      fila.style.display = nombre.includes(texto) ? '' : 'none';
    });
  });
});

function mostrarJugadores(jugadores) {
  const tbody = document.getElementById('jugadores-tbody');
  tbody.innerHTML = '';

  jugadores.forEach(jugador => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="px-4 py-2">${jugador.nombre_completo}</td>
      <td class="px-4 py-2">${jugador.categoria?.nombre || '-'}</td>
      <td class="px-4 py-2 hidden sm:table-cell">${jugador.posicion || '-'}</td>
      <td class="px-4 py-2 hidden sm:table-cell">${jugador.numero_playera || '-'}</td>
      <td class="px-4 py-2 hidden sm:table-cell">${jugador.telefono_tutor || '-'}</td>
      <td class="px-4 py-2">
        <div class="flex items-center gap-3 justify-center">
          <button class="icon-btn ver-jugador" title="Ver jugador" data-id="${jugador.id}">
            <i data-lucide="eye" class="lucide-icon text-gray-700 dark:text-white"></i>
          </button>
          <button class="icon-btn editar-jugador" title="Editar jugador" data-id="${jugador.id}">
            <i data-lucide="pencil" class="lucide-icon text-gray-700 dark:text-white"></i>
          </button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
  lucide.createIcons();
}

function agregarEventosVer(jugadores) {
  const botonesVer = document.querySelectorAll('.ver-jugador');

  botonesVer.forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      const jugador = jugadores.find(j => j.id == id);
      abrirModalJugador(jugador);
    });
  });
}

function abrirModalJugador(jugador) {
  const modal = document.getElementById('modal-jugador');
  modal.classList.remove('hidden');
  modal.classList.add('flex');

  document.getElementById('foto-modal').src = jugador.foto || 'img/elite_logo.png.png';
  const modalBody = modal.querySelector('.space-y-2');
  modalBody.innerHTML = '';

  const fechaFormateada = jugador.fecha_nacimiento ? new Date(jugador.fecha_nacimiento).toLocaleDateString('es-MX') : '-';
  const tallaPlayera = jugador.talla_playera || '-';
  const shortOLicra = jugador.talla_short || jugador.talla_licra || '-';
  const esShort = jugador.talla_short ? ` ${jugador.talla_short}` : '';
  const esLicra = jugador.talla_licra ? ` ${jugador.talla_licra}` : '';

  const campos = [
    { label: 'Nombre', value: jugador.nombre_completo },
    { label: 'Fecha Nacimiento', value: fechaFormateada },
    { label: 'Categoría', value: jugador.categoria?.nombre || '-' },
    { label: 'Posición', value: jugador.posicion || '-' },
    { label: 'Número de Playera', value: jugador.numero_playera || '-' },
    { label: 'Talla Playera', value: tallaPlayera },
    { label: 'Talla Short', value: esShort },
    { label: 'Talla Licra', value: esLicra },
    { label: 'Teléfono del tutor', value: jugador.telefono_tutor || '-' },
    { label: 'Observaciones', value: jugador.observaciones || 'Sin observaciones' },
    { label: 'Entrenador', value: jugador.entrenador?.nombre_completo || '-' },
  ];

  campos.forEach(({ label, value }) => {
    const p = document.createElement('p');
    p.innerHTML = `<strong>${label}:</strong> ${value}`;
    modalBody.appendChild(p);
  });

  if (jugador.curp) {
    const curpLink = document.createElement('p');
    curpLink.innerHTML = `<strong>CURP:</strong> <a href="${jugador.curp}" download class="text-blue-600 hover:underline" target="_blank">Descargar</a>`;
    modalBody.appendChild(curpLink);
  }

  if (jugador.acta_nacimiento) {
    const actaLink = document.createElement('p');
    actaLink.innerHTML = `<strong>Acta Nac.:</strong> <a href="${jugador.acta_nacimiento}" download class="text-blue-600 hover:underline" target="_blank">Descargar</a>`;
    modalBody.appendChild(actaLink);
  }

  const botonesExtras = document.createElement('div');
  botonesExtras.classList.add('mt-4', 'flex', 'justify-end', 'gap-2');
  botonesExtras.innerHTML = `
    <button class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 transition text-sm editar-modal" data-id="${jugador.id}">Editar</button>
    <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition text-sm eliminar-modal" data-id="${jugador.id}">Eliminar</button>
  `;
  modalBody.appendChild(botonesExtras);
  // 🗑️ Eliminar jugador
  botonesExtras.querySelector('.eliminar-modal').addEventListener('click', async () => {
    const confirmar = confirm(`¿Estás seguro de que deseas eliminar a ${jugador.nombre_completo}?`);
  
    if (!confirmar) return;
  
    try {
      const token = localStorage.getItem('access') || localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/api/jugadores/${jugador.id}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
    
      if (!response.ok) throw new Error('Error al eliminar jugador');
    
      alert('Jugador eliminado correctamente');
      document.getElementById('modal-jugador').classList.add('hidden');
    
      // Recarga la lista de jugadores
      const nuevaRespuesta = await fetch('http://127.0.0.1:8000/api/jugadores/', {
        headers: {
          Authorization: `Bearer ${token}`,
        }
      });
      const jugadoresActualizados = await nuevaRespuesta.json();
      mostrarJugadores(jugadoresActualizados);
      agregarEventosVer(jugadoresActualizados);
    
    } catch (error) {
      console.error('Error al eliminar:', error);
      alert('No se pudo eliminar el jugador.');
    }
  });
  

  document.getElementById('cerrar-modal').addEventListener('click', () => {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  });
}
