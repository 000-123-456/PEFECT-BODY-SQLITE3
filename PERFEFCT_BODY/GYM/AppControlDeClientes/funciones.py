import random
from GYM.settings import STATIC_URL
from datetime import datetime
# Define una lista de imágenes aleatorias para hombres y mujeres
imagenes_hombre = [
    '{}{}'.format(STATIC_URL,'assets/img/avatares/hombre/1M.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/hombre/2M.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/hombre/3M.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/hombre/4M.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/hombre/5M.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/hombre/6M.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/hombre/7M.jpeg'),
   
    # Agrega más URLs de imágenes para hombres
]

imagenes_mujer = [
    '{}{}'.format(STATIC_URL,'assets/img/avatares/mujer/1H.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/mujer/2H.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/mujer/3H.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/mujer/4H.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/mujer/5H.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/mujer/6H.jpeg'),
    '{}{}'.format(STATIC_URL,'assets/img/avatares/mujer/7H.jpeg'),
]

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