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

// Obtener botón para abrir modal
const btnVerHistorial = document.getElementById('btnVerHistorial');
const btnAbrirModal = document.getElementById('btnMantenimiento');
const btnAbrirModalFinalizar = document.getElementById('btnFinMantenimiento');

// Agregar listener al click  -----------------------------------------------------------------------
if(btnAbrirModal){
  btnAbrirModal.addEventListener('click', function() {
    const filaSeleccionada = obtenerFilaSeleccionada();          // Obtener fila seleccionada
    const idMaquina = filaSeleccionada.dataset.id;               // Obtener id de la fila
    console.log('idMaquina:', idMaquina);
    document.getElementById('maquinariaID').value = idMaquina;   // Asignar id al campo oculto del modal
  });
}

// Agregar listener al click  -----------------------------------------------------------------------
if(btnAbrirModalFinalizar){
btnAbrirModalFinalizar.addEventListener('click', async function() {
  const filaSeleccionada = obtenerFilaSeleccionada();          // Obtener fila seleccionada
  const idMaquina = filaSeleccionada.dataset.id;               // Obtener id de la fila
  console.log('idMaquina:', idMaquina);

  //obtener el ultimo historial de la maquina
  const idHistorial = await obtenerUltimoHistorial(idMaquina);
  console.log('idHistorial:', idHistorial);
  
  document.getElementById('historialID').value = idHistorial;   // Asignar id al campo oculto del modal
  document.getElementById('maquinaID').value = idMaquina;   // Asignar id al campo oculto del modal
});}

//---------------------------------------------------------------------------------------------------
function obtenerFilaSeleccionada() {
  const btn = event.target;                                     // Obtener botón presionado
  return btn.closest('tr');                                     // Buscar fila que lo contiene
}

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
if(btnVerHistorial){
  btnVerHistorial.addEventListener('click', function() {
    const filaSeleccionada = obtenerFilaSeleccionada();          // Obtener fila seleccionada
    const idMaquina = filaSeleccionada.dataset.id;               // Obtener id de la fila
    console.log('idMaquina:', idMaquina);
    window.location.href = "../Historial/Lista/" + idMaquina + "/"
  });
}

//---------------------------------------------------------------------------------------------------
// Obten el campo de entrada por su id
let campoFechaFin = document.getElementById('fecha_fin');
let campoFechaInicio = document.getElementById('fecha_ini');
// Obtiene la fecha actual en formato YYYY-MM-DD
let fechaActual = new Date();
// Resta un día a la fecha actual
fechaActual.setDate(fechaActual.getDate() - 1);
// Convierte la fecha a formato YYYY-MM-DD
let fechaAnterior = fechaActual.toISOString().slice(0, 10);
// Establece la fecha anterior en el campo de entrada
campoFechaFin.value = fechaAnterior;
campoFechaInicio.value = fechaAnterior;


