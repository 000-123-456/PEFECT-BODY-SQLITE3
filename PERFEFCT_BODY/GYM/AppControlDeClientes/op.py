opTipo = (
    (1, 'REGULAR'),
    (2, 'MIEMBRO')
)
opGenero = (
    (1, 'Masculino'),
    (2, 'Femenino')
)

opDia = (
    (1, 'Lunes'),
    (2, 'Martes'),
    (3, 'Miercoles'),
    (4, 'Jueves'),
    (5, 'Viernes'),
    (6, 'Sabado'),
    (7, 'Domingo'),
   
)
opRango = (
    (1, '1500 kcal'),
    (2, '2000 kcal'),
    (3, '2500 kcal'),
    (4, '3000 kcal'),
    (5, '3500 kcal'),
    (6, '4000 kcal'),
    (7, '4500 kcal'),
)
opTiempo = (
    (1, 'Merienda'),
    (2, 'Desayuno'),
    (3, 'Refrigerio de media mañana'),
    (4, 'Almuerzo'),
    (5, 'Refrigerio de media tarde'),
    (6, 'Cena'),
    (7, 'Refrigerio de noche'),
)

factor_hombres = [
    [16, 'Sedentario'],
    [21, 'Moderado'],
    [26, 'Muy activa'],  
]
factor_mujeres = [
    [14, 'Sedentario'],
    [18, 'Moderado'],
    [22, 'Muy activa'],  
]



#***************************************************************************
opExperiencia = [
    [0,'----------'],
    [1, 'Principiante'],
    [2, 'Intermedio'],
    [3, 'Avanzado'],  
]

opTipoEjercicio = [
    [0,'----------'],
    [1, 'Abdomen'],
    [2, 'Biceps'],
    [3, 'Espalda'],
    [4, 'Hombros'],
    [5, 'Pectorales'],  
    [6, 'Piernas'],  

]

opMusculo = [
   
    [1, 'Abdomen'],
    [2, 'Biceps'],
    [3, 'Espalda'],
    [4, 'Hombros'],
    [5, 'Pectorales'],  
    [6, 'Piernas'],  

]


# clave_segura.py
listFactorDeActividadMujeres= []

import secrets
import string

def generar_clave_temporal_segura():
    # Define los conjuntos de caracteres
    caracteres_especiales = string.punctuation  # Caracteres especiales
    letras_mayusculas = string.ascii_uppercase  # Letras mayúsculas
    letras_minusculas = string.ascii_lowercase  # Letras minúsculas
    digitos = string.digits  # Números

    while True:
        clave_temporal = ''.join(secrets.choice(caracteres_especiales) +
                                secrets.choice(letras_mayusculas) +
                                secrets.choice(letras_minusculas) +
                                secrets.choice(digitos) +
                                secrets.choice(caracteres_especiales) +
                                secrets.choice(letras_minusculas) +
                                secrets.choice(digitos) +
                                secrets.choice(letras_minusculas))
        clave_temporal = ''.join(secrets.SystemRandom().sample(clave_temporal, len(clave_temporal)))
        if (any(c in clave_temporal for c in caracteres_especiales) and
            any(c in clave_temporal for c in letras_mayusculas) and
            any(c in clave_temporal for c in letras_minusculas) and
            any(c in clave_temporal for c in digitos) and
            len(clave_temporal) == 8):
            return clave_temporal


rango = [1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]