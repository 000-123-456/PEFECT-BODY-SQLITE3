var selectedMemberId;
$(document).ready(function() {
    $("#btnMarcarAsistenciaMiembro").prop("disabled", true);
    $("#btnMarcarAsistenciaCliente").prop("disabled", true);

    $('#btnMarcarAsistenciaMiembro').on('click', function() {
        // Verificar si se ha seleccionado un miembro
        if (selectedMemberId) {
            $.ajax({
                url: "/Asistencia/marcar_asistencia/",
                type: "POST",
                async: false,
                data: {
                    member_id: selectedMemberId
                },
                success: function(response) {
                    // manejar respuesta
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error("Error en la solicitud AJAX: " + status + ", " + error);
                }
                
            });
            
        }else{
            // Mostrar mensaje de error (puedes usar una alerta, un elemento en el DOM, etc.)
            alert('Por favor, selecciona un miembro.');
            return; // Salir de la función para evitar enviar la solicitud AJAX sin un miembro seleccionado
        }
        
    });

    // Inicializar select2
    $(".select2").select2({
        
        ajax: {
            url: "/Asistencia/listaMiembros/",
            dataType: 'json',
            delay: 250,
            async: false,
            
            data: function(params) {
                return {
                    q: params.term // término de búsqueda
                };
            },
            
            processResults: function(data) {
                // Verificar si no hay resultados
                if (data.length === 0) {
                    // Mostrar mensaje cuando no se encuentran resultados
                    return {
                        results: [{ id: null, text: 'No se encontraron resultados' }]
                    };
                }
                // parsear datos del servidor
                return {
                    results: data
                };
            },

            
        },
        
            templateResult: formatoOpcion, // usar formatoOpcion
            templateSelection: formatRepoSelection,

    });

    //verificar si ha presionado alguna tecla en el input nombreCliente
    $('#nombreCliente').on('keyup', function() {
        if($('#nombreCliente').val().length > 3){
            $("#btnMarcarAsistenciaCliente").prop("disabled", false);
        }else{
            $("#btnMarcarAsistenciaCliente").prop("disabled", true);
        }
    });

    $('#btnMarcarAsistenciaCliente').on('click', function() {
        $.ajax({
            url: "/Asistencia/marcar_asistencia/",
            type: "POST",
            async: false,
            data: {
                nombre: $('#nombreCliente').val(),
            },
            success: function(response) {
                // manejar respuesta
                location.reload(); 
            }
        });
    
    });

});


function formatoOpcion(opcion) {
    if(!opcion.id) {
        return opcion.id;
    }
    var $opcion = $(
        '<div class="wrapper container">'+
            '<div class="row">'+
                '<div class="col-lg-2">'+
                    '<img src="' + opcion.foto + '" class="img-fluid d-block mx-auto" style="border-radius: 20px; object-fit: contain;">'+
                '</div>'+
                '<div class="col-lg-10 text-left shadow-sm">'+
                    '<p style="margin-bottom: 0;">'+
                        '<b>Nombre:</b> ' + opcion.nombre + '<br>'+
                        '<b>Apellido:</b> ' + opcion.apellido + '<br>'+
                        '<b>Edad:</b> ' + opcion.edad + ' años<br>'+
                    '</p>'+
                '</div>'+
            '</div>'+
        '</div>'

    ); 
    return $opcion;
}
function formatRepoSelection (opcion) {
    // Almacenar el ID del miembro seleccionado
 
    selectedMemberId = opcion.id;
    console.log(selectedMemberId);

    $("#btnMarcarAsistenciaMiembro").prop("disabled", false);
    var $opcion = $(
        '<div class="wrapper container">'+
            '<div class="row">'+
                '<div class="col-lg-2">'+
                    '<img src="' + opcion.foto + '" class="img-fluid d-block mx-auto" style="border-radius: 25px; object-fit: contain; width: 85%; height: 85%; padding-top: 5px;">'+
                '</div>'+
                '<div class="col-lg-10 text-left shadow-sm">'+
                    '<p style="margin-bottom: 0;">'+
                        '<b>' + opcion.nombre + ' ' + opcion.apellido + '</b> <br>'+ 
                        opcion.edad + ' años<br>'+
                    '</p>'+
                '</div>'+
            '</div>'+
        '</div>'

    ); 
    return $opcion;
   
}
