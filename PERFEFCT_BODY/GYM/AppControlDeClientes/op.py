opTipo = (
    (1, 'REGULAR'),
    (2, 'MIEMBRO')
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
# clave_segura.py

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
print(generar_clave_temporal_segura())