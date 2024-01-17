var selectedProductId;
var selectedProductName;
var selectedCantidad;
var selectedPrecio;
var total = 0;
const data=[];
const tbodyCarrito = document.getElementById('tbody-carrito');

$(document).ready(function() {

    $("#btnCarrito").prop("disabled", true);
    $("#id_cantidad").prop("disabled", true);
    $("#btnVenta").prop("disabled", true);
    $("#id_subtotal").val(0);


    $("#btnVenta").click(function(){
        console.log(data);  // Agrega este console.log para verificar el contenido de 'data'
        $.ajax({
            url: "/Venta/registroVenta/",
            type: "POST",
            contentType: 'application/json; charset=utf-8',  // Asegúrate de establecer el tipo de contenido
            data: JSON.stringify({ carrito: data }),  // Convierte el array a una cadena JSON
            success: function(response) {
                // Manejar la respuesta del servidor
                location.reload();
            },
            error: function(xhr, status, error) {
                console.error("Error en la solicitud AJAX: " + status + ", " + error);
            }
        });
    });



    // Inicializar select2
    $(".select2").select2({
            
        ajax: {
            url: "/Venta/listaProductos/",
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

    $("#id_cantidad").keydown(function(event) {
        if (event.key === ".") {
            event.preventDefault();
        }
        //evitar que se seleccione un producto con 0 unidades o que coloque 0 a al izquierda
        if (event.key === "0" && $(this).val() === "") {
            event.preventDefault();
        }
    });
    $("#id_cantidad").on('input', function(){
        validarCarritoporCantidad();
       });

    //si id cantidad cambia
    $("#id_cantidad").change(function(){
        $("#id_subtotal").val($(this).val() * selectedPrecio);
    });

    const carritoButton = document.getElementById('btnCarrito');
    
    carritoButton.addEventListener('click', () => {
        total = 0;
        //buscar si el producto ya está en el carrito
        let index = data.findIndex(x => x.id === parseInt(selectedProductId));
        if(index !== -1){
            //si ya está en el carrito, sumarle la cantidad
            data[index].cantidad = parseInt(data[index].cantidad) + parseInt($("#id_cantidad").val());
            selectedCantidad = parseInt(selectedCantidad) - parseInt($("#id_cantidad").val());
            data[index].subtotal = parseInt(data[index].cantidad) * parseFloat($("#id_precio").val());
        }else{
            data.push({
                id: parseInt(selectedProductId),
                num: data.length + 1,
                producto: selectedProductName,
                cantidad: parseInt($("#id_cantidad").val()),
                precio: parseFloat($("#id_precio").val()),
                subtotal: parseFloat($("#id_subtotal").val()),
            });
            selectedCantidad = parseInt(selectedCantidad) - parseInt($("#id_cantidad").val());
            if(selectedCantidad < parseInt($("#id_cantidad").val())){
                $("#id_cantidad").val(selectedCantidad);
            }
        }
        llenarTabla();

        validarCarritoporCantidad();
        $("#btnVenta").prop("disabled", false);
    });

});
    function validarCarritoporCantidad(){
        let cantidad = $("#id_cantidad").val();
        let stock = selectedCantidad;
         
        if(parseInt(cantidad) > parseInt(stock) || $("#id_cantidad").val() === ""){
           $("#btnCarrito").prop('disabled', true);
            $("#id_subtotal").val(0);
        } else {
           $("#btnCarrito").prop('disabled', false);
           $("#id_subtotal").val($("#id_cantidad").val() * selectedPrecio);
        }
    }

    function llenarTabla(){
        console.log(data);
        
        tbodyCarrito.innerHTML = ''; // Clear the table body
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
            <td>${item.num}</td>
            <td>${item.producto}</td>
            <td>${item.cantidad}</td>
            <td>$${item.precio}</td>
            <td>$${item.subtotal}</td>
            <td><a class='btn btn-danger btn-sm' onclick='deleteProduct(${data.indexOf(item)})'><i class='bi bi-trash'></i></a></td>
            `;

            tbodyCarrito.appendChild(row);
            total += parseFloat(item.subtotal);
        });
        $("#id_total").val(totalVenta());
    }

    function deleteProduct(index) {
        //si el id del producto a eliminar es igual al seleccionado en el select2 sumarle la cantidad al stock
        if(data[index].id === selectedProductId){
            selectedCantidad = parseInt(selectedCantidad) + parseInt(data[index].cantidad);
        }
    
        validarCarritoporCantidad();

        $("#id_total").val(totalVenta());

        data.splice(index, 1);
        if(data.length === 0){
            $("#btnVenta").prop("disabled", true);
        }
        llenarTabla();
    }

    function totalVenta(){
        let total = 0;
        data.forEach(item => {
            total += parseFloat(item.subtotal);
        });
        return total;
    }

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
                            opcion.nombre + '<br>'+
                            (opcion.descripcion == null ? "Sin descripción" : opcion.descripcion) + '<br>'+
                            opcion.cantidad + ' unidades disponibles<br>'+
                        '</p>'+
                    '</div>'+
                '</div>'+
            '</div>'

        ); 
        return $opcion;
    }
    function formatRepoSelection (opcion) {
        // si no hay suficientes unidades poner la cantidad máxima disponible
        if($("#id_cantidad").val() > opcion.cantidad){
            $("#id_cantidad").val(opcion.cantidad);
        }
        //imprimir el array de productos
        console.log(opcion);
        console.log(data);

        selectedProductId = opcion.id;
        selectedCantidad = opcion.cantidad;
        selectedPrecio = opcion.precio;
        selectedProductName = opcion.nombre;

        //calucular subtotal
        $("#id_subtotal").val($("#id_cantidad").val() * opcion.precio);

        //buscar en el carrito si ya está el producto y cuantas unidades tiene
        let index = data.findIndex(x => x.id === opcion.id);
        if(index !== -1){
            selectedCantidad = parseInt(selectedCantidad) - parseInt(data[index].cantidad);
        }
        validarCarritoporCantidad();

        $("#id_cantidad").prop("disabled", false);
        $('#id_precio').val(opcion.precio);
        var $opcion = $(
            '<div class="wrapper container">'+
                '<div class="row">'+
                    '<div class="col-lg-2">'+
                        '<img src="' + opcion.foto + '" class="img-fluid d-block mx-auto" style="border-radius: 25px; object-fit: contain; width: 85%; height: 85%; padding-top: 5px;">'+
                    '</div>'+
                    '<div class="col-lg-10 text-left shadow-sm">'+
                        '<p style="margin-bottom: 0;">'+
                            '<b>' + opcion.nombre + '</b> <br>'+ 
                            opcion.cantidad + ' disponibles<br>'+
                        '</p>'+
                    '</div>'+
                '</div>'+
            '</div>'

        ); 
        return $opcion;
    
    }

