function eliminarHistorial(id) {
  console.log('Eliminar Historial - id:', id);
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
      window.location.href = "../../Eliminar/" + id + "/"
    }
  })
}

