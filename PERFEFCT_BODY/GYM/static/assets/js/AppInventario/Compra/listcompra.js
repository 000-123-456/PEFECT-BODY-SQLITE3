function eliminarCompra(id){
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-primary',
      cancelButton: 'btn btn-danger'
    },
    buttonsStyling: false
  })
  
  swalWithBootstrapButtons.fire({
    title: '¿Seguro que desea eliminar la compra?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Confirmar!',
    cancelButtonText: 'Cancelar!',
    reverseButtons: true
  }).then((result) => {
    if (result.isConfirmed) {
      
      window.location.href = "EliminarCompra/"+id+"/"
    } else if (
      /* Read more about handling dismissals below */
      result.dismiss === Swal.DismissReason.cancel
    ) {
      swalWithBootstrapButtons.fire(
        'Operación cancelada',
        'La compra no se ha eliminado  :)',
        'error'
      )
    }
  })
}
let obtenerCompra = async (nombre) => {
  try {
    const response = await fetch(`./get_compra/${nombre}/`)
    const data = await response.json()
    if(data.message === 'success'){
      inputs[1].innerText = data.nombre.toUpperCase()
      inputs[2].innerText = data.producto
      inputs[3].innerText = data.proveedor
      inputs[4].innerText = data.precio_unitario
      inputs[5].innerText = data.fecha_vec
   
      
    }
  } catch (error) {

  }
}
const tabla = document.getElementById("data")
const inputs = document.querySelectorAll(".verC")
tabla.addEventListener('click',(e) => {
  e.stopPropagation();
  //console.log(e.target.class)
  if(e.target.classList.contains('btnVP')){
      let data = e.target.parentElement.parentElement.children;
      console.log(data[1].innerText)
      obtenerCompra(data[1].innerText)
      console.log(inputs)
      //fill(data)
  }
  if(e.target.classList.contains('iVP')){
      let data = e.target.parentElement.parentElement.parentElement.children;
      console.log(data[1].innerText)
      obtenerCompra(data[1].innerText)

      //fill(data)
  }
  
 
})
