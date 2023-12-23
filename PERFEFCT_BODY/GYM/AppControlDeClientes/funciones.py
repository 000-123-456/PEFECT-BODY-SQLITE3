import random
from GYM.settings import STATIC_URL,BASE_DIR
from datetime import datetime, timedelta,date
from AppControlDeClientes.models import Miembro
from django.templatetags.static import static
import os
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from .models import Dieta, VentaMembresia


# Directorio que contiene las imágenes
directorio_hombre = os.path.join(BASE_DIR, 'static', 'assets', 'img', 'avatares', 'hombre')
directorio_mujer = os.path.join(BASE_DIR, 'static', 'assets', 'img', 'avatares', 'mujer')


# Extensiones de archivo de imágenes permitidas
extensiones_imagen = ('.jpg', '.jpeg', '.png', '.gif')

# Lista para almacenar las URLs de las imágenes
imagenes_hombre = []
imagenes_mujer= []
# Recorre los archivos en el directorio
# Recorre los archivos en el directorio
for nombre_archivo in os.listdir(directorio_hombre):
    # Obtiene la extensión del archivo
    _, extension = os.path.splitext(nombre_archivo)
    extension = extension.lower()  # Convierte a minúsculas

    # Verifica si la extensión corresponde a una imagen
    if extension in extensiones_imagen:
        # Construye la URL completa y la agrega a la lista
        url_imagen = '{}{}'.format(STATIC_URL, os.path.join('assets/img/avatares/hombre/', nombre_archivo))
        imagenes_hombre.append(url_imagen)

#obtner archivos de mujeres
for nombre_archivo in os.listdir(directorio_mujer):
    # Obtiene la extensión del archivo
    _, extension = os.path.splitext(nombre_archivo)
    extension = extension.lower()  # Convierte a minúsculas

    # Verifica si la extensión corresponde a una imagen
    if extension in extensiones_imagen:
        # Construye la URL completa y la agrega a la lista
        url_imagen = '{}{}'.format(STATIC_URL, os.path.join('assets/img/avatares/mujer/', nombre_archivo))
        imagenes_mujer.append(url_imagen)

# Ahora, 'urls_imagenes' contiene las URLs de todas las imágenes en el directorio

# Define una lista de imágenes aleatorias para hombres y mujeres


def obtener_url_imagen(genero):
    if genero == 1:
        return random.choice(imagenes_hombre)
    elif genero == 2:
        return random.choice(imagenes_mujer)
    else:
        return '{}{}'.format(STATIC_URL,'assets/img/no-photo.jpg')  # Devuelve una cadena vacía si el género no es válido



def calcular_edad(fecha_nacimiento):
    # Convierte la fecha de nacimiento a un objeto datetime
    fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
    
    # Obtiene la fecha actual
    fecha_actual = datetime.now()
    
    # Calcula la diferencia entre la fecha actual y la fecha de nacimiento
    edad = fecha_actual.year - fecha_nac.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nac.month, fecha_nac.day))
    
    return edad





from datetime import date, timedelta

def calcular_fecha_final(fecha_inicio, duracion):
    # Verifica si fecha_inicio es None
    if not fecha_inicio:
        return None

    # Obtiene el año y mes de la fecha de inicio
    year = fecha_inicio.year
    month = fecha_inicio.month

    # Aplica la duración en meses
    for _ in range(duracion):
        # Obtiene el último día del mes actual
        ultimo_dia_mes_actual = (date(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        # Determina el año y mes del mes siguiente
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

        # Obtiene el último día del mes siguiente
        ultimo_dia_mes_siguiente = (date(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Calcula el día para la fecha final
        if fecha_inicio.day <= ultimo_dia_mes_siguiente.day:
            day = fecha_inicio.day
        else:
            day = ultimo_dia_mes_siguiente.day

    # Calcula la fecha final
    fecha_final = date(year, month, day)

    return fecha_final

# Uso de la función:
fecha_inicio = date(2023, 10, 27)  # Reemplaza con tu fecha de inicio como objeto date
duracion_meses = 1  # Reemplaza con la duración en meses que desees
fecha_final = calcular_fecha_final(fecha_inicio, duracion_meses)
print(fecha_final)  # Esto imprimirá la fecha final

def vencimientoMembresias():
        try:
        # Obtén la fecha actual
            fecha_actual = date.today()

            # Filtra los miembros con fecha_fin menor a la fecha actual y estado igual a 0
            miembros_por_actualizar = Miembro.objects.filter(fecha_fin__lt=fecha_actual, estado=0)

            # Verifica si hay miembros para actualizar
            if miembros_por_actualizar.exists():
                # Actualiza el campo estado_membresia a 2 para estos miembros
                miembros_por_actualizar.update(estado_membresia=2, venta_activa=None)
                print("Los miembros han sido actualizados.")
            else:
                print("No se encontraron miembros que cumplan con los criterios de filtrado.")

        except Exception as e:
            print(f"Ocurrió un error: {e}")

def getVentasMensuales():


    # Realiza una consulta para obtener la suma de monto_pagado agrupada por mes y membresía
    ventas_por_mes = VentaMembresia.objects.values('membresia__nombre').annotate(
        mes=ExtractMonth('fecha'),
        anio=ExtractYear('fecha'),
        total_venta=Sum('monto_pagado')
    ).order_by('membresia__nombre', 'anio', 'mes')

    # Estructura los datos como se muestra en el ejemplo
    series = []

    # Crear una lista de 12 meses con valores iniciales en 0
    months = [0] * 12

    current_membresia = None
    current_year = None
    data = []

    for venta in ventas_por_mes:
        if current_membresia != venta['membresia__nombre'] or current_year != venta['anio']:
            if current_membresia:
                series.append({
                    'name': current_membresia,
                    'data': data,
                })
            current_membresia = venta['membresia__nombre']
            current_year = venta['anio']
            data = [0] * 12
        data[venta['mes'] - 1] = venta['total_venta']

    # Agrega el último conjunto de datos
    if current_membresia:
        series.append({
            'name': current_membresia,
            'data': data,
        })
    return series
def getCantidadVentas():
    # Realiza la consulta y agrupa por el campo 'nombre' de la membresía y cuenta cuántas veces se ha vendido
    data = VentaMembresia.objects.values('membresia__nombre').annotate(cantidad=Count('id'))

    # Convierte el resultado en el formato deseado
    series_data = []
    for item in data:
        series_data.append({'name': item['membresia__nombre'], 'data': item['cantidad']})
    return series_data
# Ahora, 'series_data' contiene la estructura que mencionaste
jsonPruebas = {
    "success":True,
  "dietas": [
    {
      "nombre": "Dieta 1",
      "comidas": [
        {
          "tipo": "Desayuno",
          "imagen": "URL_DE_IMAGEN",
          "descripcion": "1 Huevo frito con 1 cucharada de queso cheddar.",
          "calorias": 200
        },
        {
          "tipo": "Merienda",
          "imagen": "URL_DE_IMAGEN",
          "descripcion": "1 taza de tutifrutis.",
          "calorias": 250
        },
        {
          "tipo": "Almuerzo",
          "imagen": "URL_DE_IMAGEN",
          "descripcion": "5 onzas de pollo a la plancha, 1 taza de ensalada de vegetales.",
          "calorias": 300
        },
        
      ]
    },
    {
      "nombre": "Dieta 2",
      "comidas": [
        {
          "tipo": "Desayuno",
          "imagen": "URL_DE_IMAGEN",
          "descripcion": "Omelette de huevo con jamón:1 huevos enteros + 1 lasca de jamón de pavo (sal y pimienta al gusto).\n½ taza de vegetales crudos (lechuga, tomate, rábano, pepino).",
          "calorias": 250
        },
        {
          "tipo": "Merienda",
          "imagen": "URL_DE_IMAGEN",
          "descripcion": "2/3 de taza de yogurt con 6 fresas.",
          "calorias": 200
        },
        {
          "tipo": "Almuerzo",
          "imagen": "URL_DE_IMAGEN",
          "descripcion": "5 onza de pollo a la plancha, 1 taza de ensalada de vegetales, 1 taza de arroz, 2 tortillas o panes y 1 vaso de jugo de naranja con 3 cucharaditas de azúcar.",
          "calorias": 300
        },
        {
          "tipo": "Merienda",
          "imagen": "URL_DE_IMAGEN",
          "descripcion": "1 barra de granola, 1 guineo mediano.",
          "calorias": 150
        },
        {
          "tipo": "Cena",
          "imagen": "URL_DE_IMAGEN",
          "descripcion": "1 ½ taza de pasta con ½ taza de vegetales salteado..",
          "calorias": 200
        },
        
      ]
    }
   
  ]
}

def encontrar_posicion_mas_cercana(array, objetivo, valor):
    minimo = min(array)
    maximo = max(array)

    if objetivo == 1 and valor < minimo:
        return 1  # Devuelve la posición más uno del valor mínimo
    elif objetivo == 2 and valor > maximo:
        return len(array)  # Devuelve la posición más uno del valor máximo
    if objetivo == 1:
        valores_por_debajo = [x for x in array if x <= valor]
        return array.index(max(valores_por_debajo)) + 1
    elif objetivo == 2:
        valores_por_encima = [x for x in array if x >= valor]
        return array.index(min(valores_por_encima)) + 1

from django.http import JsonResponse
from django.forms.models import model_to_dict

def obtener_comidas_por_dieta(rango):
    # Filtrar las dietas por el rango proporcionado
    dietas = Dieta.objects.filter(rango=rango)

    # Obtener todas las comidas relacionadas con esas dietas y convertirlas a diccionarios
    comidas_por_dieta = []

    for dieta in dietas:
        comidas = dieta.comida_set.all().order_by('tiempo')  # Ordenar las comidas por el campo 'tiempo'
        comidas_dict = {
            'nombre': dieta.nombre,
            'comidas': [comida.toJSON() for comida in comidas]
        }
        comidas_por_dieta.append(comidas_dict)

    # Devolver la respuesta en formato JSON
    return {'dietas': comidas_por_dieta, 'success': True}




