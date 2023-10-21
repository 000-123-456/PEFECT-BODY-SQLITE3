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
  let obtenerProducto = async (usuario) => {
    try {
      const response = await fetch(`./get_miembro/${usuario}/`)
      const data = await response.json()
      if(data.message === 'success'){
        console.log(data)
        inputs[0].src = data.foto
        inputs[1].innerText = data.nombre.toUpperCase()
        inputs[2].innerText = data.edad
        inputs[3].innerText = data.genero
        inputs[4].innerText = data.email
        if(data.nombreContact || data.telefonoContact){
          inputs[5].innerText = data.nombreContact.toString() + " "+data.telefonoContact.toString() 
        }else{
          inputs[5].innerText ="No ingresado"
        }
       
        if(data.estado_membresia===0){
          inputs[6].classList.remove('bg-danger')
          inputs[6].classList.remove('bg-success')
          inputs[6].innerText = "No asignada"
          inputs[6].classList.add('bg-danger')
        }else if(data.estado_membresia===1){
          inputs[6].classList.remove('bg-danger')
          inputs[6].classList.remove('bg-success')
          inputs[6].innerText = "ACTIVA"
          inputs[6].classList.add('bg-success')
          inputs[7].innerText = "finaliza el "+data.fecha_fin


        }else{
          inputs[6].classList.remove('bg-success')
          inputs[6].classList.remove('bg-danger')
          inputs[6].innerText = "VENCIDA"
          inputs[6].classList.add('bg-danger')
        }
        inputs[8].innerText = data.direcccion || "No ingresada"
        inputs[9].innerText = data.telefono || "No ingresado"

        
        
        
       
        
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
        obtenerProducto(data[2].innerText)
        console.log(inputs)
        //fill(data)
    }
    if(e.target.classList.contains('iVP')){
        let data = e.target.parentElement.parentElement.parentElement.children;
        console.log(data[1].innerText)
        obtenerProducto(data[2].innerText)

        //fill(data)
    }
    
   
})
