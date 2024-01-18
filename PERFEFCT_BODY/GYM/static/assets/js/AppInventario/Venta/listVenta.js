const tbodyCarrito = document.getElementById('tbody-carrito');

$(document).ready(function(){

    const botonVerProductos = document.querySelectorAll('.btnVP');

    botonVerProductos.forEach(boton => {
        boton.addEventListener('click', (e) => {
            let filaSeleccionada = obtenerFilaSeleccionada(e);
            let id = filaSeleccionada.dataset.id;
            console.log(id);
            $.ajax({
                url: '/Venta/verProductos/' + id + '/',
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                    llenarTabla(data);
                }
            });
        });
    });
});

//---------------------------------------------------------------------------------------------------
function obtenerFilaSeleccionada(evento) {
    const btn = evento.currentTarget;                                     // Obtener botón presionado
    return btn.closest('tr');                                     // Buscar fila que lo contiene
  }
  
//---------------------------------------------------------------------------------------------------

// Modificamos la función para aceptar datos como parámetro
function llenarTabla(data){
    tbodyCarrito.innerHTML = ''; // Limpiamos la tabla
    data.forEach((item, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${item.producto}</td>
            <td>${item.cantidad}</td>
            <td>$${item.precio_vendido}</td>
            <td>$${item.subtotal}</td>
        `;
        tbodyCarrito.appendChild(row);
    });
}

function eliminarVenta(id) {
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