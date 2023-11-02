function eliminarMaquina(id) {
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-primary ml-4 mr-4',
      cancelButton: 'btn btn-danger ml-4 mr-4'
    },
    buttonsStyling: false
  })

  swalWithBootstrapButtons.fire({
    title: '¿Seguro que desea eliminar?',
    text: 'Esta acción no se puede revertir!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Confirmar!',
    cancelButtonText: 'Cancelar!',
    reverseButtons: true
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = "../Eliminar/" + id + "/"
    }
  })
}

//---------------------------------------------------------------------------------------------------
function obtenerFilaSeleccionada(evento) {
  const btn = evento.currentTarget;                                     // Obtener botón presionado
  return btn.closest('tr');                                     // Buscar fila que lo contiene
}

//---------------------------------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  // Obtén todos los botones en las filas de la tabla
  const botonesMantenimiento = document.querySelectorAll('.btnMantenimiento');
  const botonesFinMantenimiento = document.querySelectorAll('.btnFinMantenimiento');
  const botonVerHistorial = document.querySelectorAll('.btnVerHistorial');

  // Agrega eventos a los botones de mantenimiento
  botonesMantenimiento.forEach(btn => {
    btn.addEventListener('click', (e) => {
      let filaSeleccionada = obtenerFilaSeleccionada(e);
      let idMaquina = filaSeleccionada.dataset.id;
      console.log('Mantenimiento - idMaquina:', idMaquina);
      document.getElementById('maquinariaID').value = idMaquina;
    });
  });

  // Agrega eventos a los botones de fin de mantenimiento
  botonesFinMantenimiento.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      let filaSeleccionada = obtenerFilaSeleccionada(e);
      let idMaquina = filaSeleccionada.dataset.id;
      console.log('Fin Mantenimiento - idMaquina:', idMaquina);
      let idHistorial = await obtenerUltimoHistorial(idMaquina);
      console.log('Fin Mantenimiento - idHistorial:', idHistorial);
      document.getElementById('historialID').value = idHistorial;
      document.getElementById('maquinaID').value = idMaquina;
    });
  });

  // Agrega eventos a los botones de ver historial
  botonVerHistorial.forEach(btn => {
    btn.addEventListener('click', (e) => {
      let filaSeleccionada = obtenerFilaSeleccionada(e);
      let idMaquina = filaSeleccionada.dataset.id;
      console.log('Ver Historial - idMaquina:', idMaquina);
      window.location.href = "../Historial/Lista/" + idMaquina + "/";
    });
  });
});

//---------------------------------------------------------------------------------------------------
const obtenerUltimoHistorial = async (idMaquina) => {
  try {
      const response = await fetch(`/HistorialMaquinaria/Ultimo/${idMaquina}`);
      const data = await response.json();
      return data.id;                           // Devuelve el campo 'id' de la respuesta JSON
  } catch (error) {
      console.error(error);                       // Maneja errores de red o errores JSON aquí
      return null;         // o maneja el error devolviendo un valor específico según tu lógica
  }
}

//---------------------------------------------------------------------------------------------------
// Obten el campo de entrada por su id
let campoFechaFin = document.getElementById('fecha_fin');
let campoFechaInicio = document.getElementById('fecha_ini');
// Obtiene la fecha actual en formato YYYY-MM-DD
let fechaActual = new Date();
// Resta un día a la fecha actual
fechaActual.setDate(fechaActual.getDate());
// Convierte la fecha a formato YYYY-MM-DD
let fechaAnterior = fechaActual.toISOString().slice(0, 10);
// Establece la fecha anterior en el campo de entrada
campoFechaFin.value = fechaAnterior;
campoFechaInicio.value = fechaAnterior;


