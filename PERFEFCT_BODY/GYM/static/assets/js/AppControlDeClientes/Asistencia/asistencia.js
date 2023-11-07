var selectedMemberId; // Variable para almacenar el ID del miembro seleccionado
$(document).ready(function() {

    // Inicializar select2
    $(".select2").select2({
        ajax: {
            url: "/Asistencia/listaMiembros/",
            dataType: 'json',
            delay: 250,
            
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
            } 
        },
            templateResult: formatoOpcion, // usar formatoOpcion
            templateSelection: formatRepoSelection
    });


    $('#btnMarcarAsistenciaMiembro').on('click', function() {
        // Verificar si se ha seleccionado un miembro
        if (!selectedMemberId) {
            // Mostrar mensaje de error (puedes usar una alerta, un elemento en el DOM, etc.)
            alert('Por favor, selecciona un miembro.');
            return; // Salir de la función para evitar enviar la solicitud AJAX sin un miembro seleccionado
        }
        $.ajax({
            url: "/Asistencia/marcar_asistencia/",
            type: "POST",
            data: {
                member_id: selectedMemberId
            },
        });
        
    });
    $('#btnMarcarAsistenciaCliente').on('click', function() {
        $.ajax({
            url: "/Asistencia/marcar_asistencia/",
            type: "POST",
            data: {
                nombre: $('#nombreCliente').val(),
            },
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
                    '<img src="' + opcion.fotoURL.replace('/media', '') + '" class="img-fluid d-block mx-auto" style="border-radius: 20px; object-fit: contain;">'+
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
    return opcion.nombre + ' ' + opcion.apellido;
}
