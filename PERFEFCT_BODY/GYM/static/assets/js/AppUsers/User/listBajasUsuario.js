function altaUsuario(id, nombre){
    const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons.fire({
      title: `¿Seguro que desea activar a ${nombre}? Podrá acceder al sistema.`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar',
      cancelButtonText: 'Cancelar',
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
        
        window.location.href = "alta/"+id+"/"
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
    { popover: { title: '¡Hola! 😊', description: 'Comenzarás un tour guiado para explicarte lo que puedes hacer en esta sección de usuarios eliminados y aclarar todas tus dudas.' } },
    { element: '.table-responsive', popover: { title: 'Listado de Usuarios Eliminados 🏋️', description: 'En esta tabla se muestra información detallada de todos los usuarios del sistema que han sido eliminados, incluyendo empleados y administradores.' , side: 'in', align: 'start' }},
    { element: '#data_filter', popover: { title: 'Buscar 🔍', description: 'Utiliza este campo para escribir y filtrar información específica de los usuarios eliminados en la tabla.' , side: 'left', align: 'start' }},
    { element: '.sorting', popover: { title: 'Ordenar Datos ↕️', description: 'Haz clic en los encabezados de la tabla para ordenar la información de los usuarios eliminados.' , side: 'right', align: 'start' }},
    { element: '#restaurar', popover: { title: 'Restaurar Usuario 🔄', description: 'Con este botón, puedes restaurar usuarios eliminados previamente. ¡Devuélvelos a la acción!' , side: 'right', align: 'start' }},
    { element: '#data_info', popover: { title: 'Información del Listado 📊', description: 'Aquí se muestra la cantidad total de usuarios eliminados y cuántos están siendo visualizados actualmente.' , side: 'right', align: 'start' }},
    { element: '#data_paginate', popover: { title: 'Páginas 📄➡️', description: 'Navega entre las páginas para ver diferentes conjuntos de usuarios eliminados en el listado.' , side: 'left', align: 'start' }},
    { popover: { title: '¡Fin del tour! 😁', description: 'Espero que esta presentación sea la que estás buscando. Puedes ver el tour las veces que gustes 😊' }}
]

 });
 
 driverObj.drive();
 }