import random

def distancia_teclas(a, b):
    teclado = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [None, 0, None]]
    try:
        xa, ya = divmod(teclado.index([c for c in teclado if a in c][0]), 1)
    except IndexError:
        xa, ya = None, None
    try:
        xb, yb = divmod(teclado.index([c for c in teclado if b in c][0]), 1)
    except IndexError:
        xb, yb = None, None
    if xa is None or xb is None:
        return float('inf')
    return ((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5

def aptitud(cadena):
    return sum(distancia_teclas(cadena[i], cadena[i+1]) for i in range(len(cadena)-1))

def generar_poblacion(tamano):
    poblacion = []
    for i in range(tamano):
        individuo = ''.join(str(random.randint(0, 9)) for j in range(9))
        poblacion.append(individuo)
    return poblacion

def seleccion(poblacion):
    return sorted(poblacion, key=aptitud, reverse=True)[:int(len(poblacion)*0.2)]

def cruzamiento(padre, madre):
    punto = random.randint(1, len(padre)-2)
    hijo1 = padre[:punto] + madre[punto:]
    hijo2 = madre[:punto] + padre[punto:]
    return hijo1, hijo2

def mutacion(individuo):
    punto = random.randint(0, len(individuo)-1)
    return individuo[:punto] + str(random.randint(0, 9)) + individuo[punto+1:]

def algoritmo_genetico(tamano_poblacion, num_generaciones):
    poblacion = generar_poblacion(tamano_poblacion)
    for i in range(num_generaciones):
        seleccionados = seleccion(poblacion)
        descendencia = []
        while len(descendencia) < tamano_poblacion - len(seleccionados):
            padre = random.choice(seleccionados)
            madre = random.choice(seleccionados)
            hijo1, hijo2 = cruzamiento(padre, madre)
            descendencia.append(hijo1)
            descendencia.append(hijo2)
        mutados = [mutacion(individuo) for individuo in descendencia]
        poblacion = seleccionados + mutados
    return max(poblacion, key=aptitud)

password = algoritmo_genetico(100, 100)
print(f"La contraseña generada es: {password}")