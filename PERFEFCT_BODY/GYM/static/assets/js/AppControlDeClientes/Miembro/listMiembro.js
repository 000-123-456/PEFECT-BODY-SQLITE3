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

  function asiganarMembresia(idusuario, idMembresia){
    const swalWithBootstrapButtons2 = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons2.fire({
      title: '¿Seguro que desea realizar esta acción?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar',
      cancelButtonText: 'Cancelar',
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
        
        window.location.href = "CrearVentaMembresia/"+idusuario+"/"+idMembresia+"/"
      } else if (
        /* Read more about handling dismissals below */
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons2.fire(
          'Operacion cancelada',
          'La membresía no se ha asigando :)',
          'error'
        )
      }
    })
  }
  let obtenerMiembro = async (usuario) => {
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
const usernameId = document.getElementById("usernameId")
const membresiaId  = document.getElementById("membresiaId")
tabla.addEventListener('click',(e) => {
    e.stopPropagation();
    //console.log(e.target.class)
    if(e.target.classList.contains('btnVP')){
        let data = e.target.parentElement.parentElement.children;
        console.log(data[1].innerText)
        obtenerMiembro(data[2].innerText)
        console.log(inputs)
        //fill(data)
    }
    if(e.target.classList.contains('iVP')){
        let data = e.target.parentElement.parentElement.parentElement.children;
        console.log(data[1].innerText)
        obtenerMiembro(data[2].innerText)

        //fill(data)
    }
    if(e.target.classList.contains('btnAM')){
      let data = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.children;
      console.log(data)
      usernameId.value = data[2].innerText
      console.log(usernameId.value)

      //fill(data)
  }
  if(e.target.classList.contains('aAM')){
    let data = e.target.parentElement.parentElement.parentElement.parentElement.children;
    console.log(data)
    usernameId.value = data[2].innerText
    console.log(usernameId.value)

    //fill(data)
}
if(e.target.classList.contains('liAM')){
  let data = e.target.parentElement.parentElement.parentElement.children;
  console.log(data)
  usernameId.value = data[2].innerText
  console.log(usernameId.value)

  //fill(data)
}
  if(e.target.classList.contains('iAM')){
    let data = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.children;
    console.log(data[2].innerText)
    usernameId.value = data[2].innerText
    console.log(usernameId.value)

}
if(e.target.classList.contains('btnAsignar')){
  let data = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.children;
  console.log(data[2].innerText)
  usernameId.value = data[2].innerText
  console.log(usernameId.value)

}

    
   
})
document.addEventListener("DOMContentLoaded", function () {
  let buttons = document.querySelectorAll("a.btnAsignar");

  buttons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      
      // Obtiene el valor del input con id "usernameId"
      var user = document.getElementById("usernameId");
      var userText = user.value;
      
      // Encuentra el elemento .price-box más cercano al botón clicado
      let priceBox = this.closest(".price-box");

      if (priceBox) {
        // Busca el input con la clase "idM" dentro del elemento priceBox
        let input = priceBox.querySelector("input.idM");

        if (input) {
          let idMembresia = input.value;
          asiganarMembresia(userText,idMembresia);
        } else {
          alert("No se encontró el input con la clase 'idM' dentro del .price-box.");
        }
      } else {
        alert("No se encontró un elemento .price-box cercano al botón clicado.");
      }
    });
  });
});
