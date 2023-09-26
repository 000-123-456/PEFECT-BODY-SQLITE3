function eliminarCategoria(id){
    const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons.fire({
      title: '¿Seguro que desea eliminar la categoría?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar!',
      cancelButtonText: 'Cancelar!',
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
        
        window.location.href = "EliminarCategoria/"+id+"/"
      } else if (
        /* Read more about handling dismissals below */
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons.fire(
          'Operación cancelada',
          'La categoría no se ha eliminado  :)',
          'error'
        )
      }
    })
  }
    const tabla = document.getElementById("data")
    const modal = document.getElementById("modificarCategoria")
    const inputs = document.querySelectorAll(".updateI")
    let count=0;
    
    tabla.addEventListener('click',(e) => {
        e.stopPropagation();
        
        //console.log(e.target.class)
        if(e.target.classList.contains('btnUC')){
          
            let data = e.target.parentElement.parentElement.children;
            console.log(data[1].innerText)
            obtenerCategoria(data[1].innerText)
            //fill(data)
        }
        if(e.target.classList.contains('iUC')){
            let data = e.target.parentElement.parentElement.parentElement.children;
            console.log(data[1].innerText)
            obtenerCategoria(data[1].innerText)

            //fill(data)
        }
        
       
    })
    let obtenerCategoria = async (nombre) => {
      try {
        const response = await fetch(`./${nombre}/`)
        const data = await response.json()
        if(data.message === 'success'){
          inputs[0].value = data.id
          inputs[1].value = data.nombre
          if(data.perecedero){
            console.log('entra')
            inputs[2].setAttribute("checked", "return true");
          }else{
            inputs[2].removeAttribute("checked")
          }

          
          

        }
      } catch (error) {
        
      }
    }
    let fill = (data)=>{
        count=0
        for(let index of inputs){
            index.value = data[count].innerText
            count+=1;
        }
    }   