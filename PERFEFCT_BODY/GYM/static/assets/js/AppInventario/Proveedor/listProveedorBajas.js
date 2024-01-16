function AltaProveedor(id){
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-primary ml-4 mr-4',
      cancelButton: 'btn btn-danger ml-4 mr-4'
    },
    buttonsStyling: false
  })
  
  swalWithBootstrapButtons.fire({
    title: '¿Seguro que desea restaurar el proveedor?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Confirmar!',
    cancelButtonText: 'Cancelar!',
    reverseButtons: true
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = "../Alta/"+id+"/"
    } else if (
      /* Read more about handling dismissals below */
      result.dismiss === Swal.DismissReason.cancel
    ) {
      swalWithBootstrapButtons.fire(
        'Operacion cancelada',
        'El proveedor no se ha restaurado  :)',
        'error'
      )
    }
  })
}
