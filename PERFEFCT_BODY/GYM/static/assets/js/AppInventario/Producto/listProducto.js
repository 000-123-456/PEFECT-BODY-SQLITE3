function eliminarProducto(id){
    const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons.fire({
      title: '¿Seguro que desea eliminar el producto?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar!',
      cancelButtonText: 'Cancelar!',
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
        
        window.location.href = "EliminarProducto/"+id+"/"
      } else if (
        /* Read more about handling dismissals below */
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons.fire(
          'Operacion cancelada',
          'El producto no se ha eliminado  :)',
          'error'
        )
      }
    })
  }
  let obtenerProducto = async (nombre) => {
    try {
      const response = await fetch(`./${nombre}/`)
      const data = await response.json()
      if(data.message === 'success'){
        inputs[0].src = data.img
        inputs[1].innerText = data.nombre.toUpperCase()
        inputs[2].innerText = '$'+data.precio_venta
        inputs[3].innerText = data.cantidad
        inputs[4].innerText = data.nivel_bajo
        inputs[5].innerText = data.categoria
        inputs[6].innerText = data.descripcion
        
      }
    } catch (error) {

    }
  }
const tabla = document.getElementById("data")
const inputs = document.querySelectorAll(".verP")
tabla.addEventListener('click',(e) => {
    e.stopPropagation();
    //console.log(e.target.class)
    if(e.target.classList.contains('btnVP')){
        let data = e.target.parentElement.parentElement.children;
        console.log(data[1].innerText)
        obtenerProducto(data[1].innerText)
        console.log(inputs)
        //fill(data)
    }
    if(e.target.classList.contains('iVP')){
        let data = e.target.parentElement.parentElement.parentElement.children;
        console.log(data[1].innerText)
        obtenerProducto(data[1].innerText)

        //fill(data)
    }
    
   
})
