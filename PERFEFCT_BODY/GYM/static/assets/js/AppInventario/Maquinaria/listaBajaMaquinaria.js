function altaMaquina(id){
    const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-primary ml-4 mr-4',
        cancelButton: 'btn btn-danger ml-4 mr-4'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons.fire({
      title: '¿Seguro que desea restaurar la máquina?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar!',
      cancelButtonText: 'Cancelar!',
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = "../Alta/"+id+"/"
      }
    })
  }

function altaTodasMaquinaria(){
    const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-primary ml-4 mr-4',
        cancelButton: 'btn btn-danger ml-4 mr-4'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons.fire({
      title: '¿Seguro que desea restaurar las máquinas?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar!',
      cancelButtonText: 'Cancelar!',
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = "../AltaTodas/"
      }
    })
  }