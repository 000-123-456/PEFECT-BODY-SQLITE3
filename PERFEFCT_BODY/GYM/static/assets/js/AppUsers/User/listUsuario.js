function eliminarUsuario(id, nombre){
    const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons.fire({
      title: `¿Seguro que desea eliminar a ${nombre}? No podrá acceder al sistema.`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar',
      cancelButtonText: 'Cancelar',
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
        
        window.location.href = "baja/"+id+"/"
      } else if (
        /* Read more about handling dismissals below */
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons.fire(
          'Operacion cancelada',
          `${nombre} no se ha eliminado  :)`,
          'error'
        )
      }
    })
  }


  //------------------Funcion de ayuda---------------------
 const driver = window.driver.js.driver;
 function tour() {
 const driverObj = driver({
   popoverClass: 'driverjs-theme',
   nextBtnText: 'Siguiente',
   prevBtnText: 'Anterior',
   doneBtnText: 'Completado',
   showButtons: [
     'next',
     'previous',
     'done'
   ],
   steps: [
   { popover: { title: '¡Hola! 😊', description: 'Comenzarás un tour guiado para explicarte lo que puedes hacer en esta sección de usuarios y aclarar todas tus dudas.' } },
   { element: '#nuevo', popover: { title: 'Nuevo Usuario ➕', description: 'Haz clic en este botón para crear un nuevo usuario.', side: 'left', align: 'start' }},
   { element: '#papelera', popover: { title: 'Papelera 🗑️', description: 'Este botón te llevará a la papelera de usuarios. Aquí podrás ver y restaurar usuarios que hayan sido dados de baja previamente.', side: 'bottom', align: 'start' }}, 
   { element: '.table-responsive', popover: { title: 'Listado de Usuarios 🏋️', description: 'En esta tabla se muestra información detallada de todos los usuarios del sistema, incluyendo empleados y administradores.', side: 'in', align: 'start' }},
   { element: '#data_filter', popover: { title: 'Buscar 🔍', description: 'Utiliza este campo para escribir y filtrar información específica de los usuarios en la tabla.', side: 'left', align: 'start' }},
   { element: '.sorting', popover: { title: 'Ordenar Datos ↕️', description: 'Haz clic en los encabezados de la tabla para ordenar la información de los usuarios.', side: 'right', align: 'start' }},
   { element: '#btn-actualizar', popover: { title: 'Actualizar Usuario 🔄', description: 'Al hacer clic en este botón, serás dirigido a la página donde podrás actualizar la información del usuario seleccionado.', side: 'right', align: 'start' }},
   { element: '#btn-eliminar', popover: { title: 'Dar de Baja 📉', description: 'Selecciona este botón para dar de baja a un usuario. Podrás restaurarlo desde la papelera si es necesario.', side: 'left', align: 'start' }},
   { element: '#data_info', popover: { title: 'Información del Listado 📊', description: 'Aquí se muestra la cantidad total de usuarios y cuántos están siendo visualizados actualmente.', side: 'right', align: 'start' }},
   { element: '#data_paginate', popover: { title: 'Páginas 📄➡️', description: 'Navega entre las páginas para ver diferentes conjuntos de usuarios en el listado.', side: 'left', align: 'start' }},
   { popover: { title: '¡Fin del tour! 😁', description: 'Espero que esta presentación sea la que estás buscando. Puedes ver el tour las veces que gustes 😊' }}
  ]
 });
 
 driverObj.drive();
 }