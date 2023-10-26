import random
from GYM.settings import STATIC_URL,BASE_DIR
from datetime import datetime, timedelta,date
from AppControlDeClientes.models import Miembro
from django.templatetags.static import static
import os


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
fecha_inicio = date(2024, 10, 31)  # Reemplaza con tu fecha de inicio como objeto date
duracion_meses = 4  # Reemplaza con la duración en meses que desees
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





















