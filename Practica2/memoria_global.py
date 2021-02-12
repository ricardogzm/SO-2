import os
import time
import threading
import memoria as m
from typing import List
from prettytable import PrettyTable


if os.name == "posix":
    var = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
    var = "cls"


def limpiar():
    os.system(var)


lista_mutex = threading.Lock()


def imprimir_tabla(lista_memoria: List[m.Bloque], lista_trabajos: List[m.Trabajo]):
    while True:
        limpiar()

        lista_mutex.acquire()
        tabla_memoria = PrettyTable()
        tabla_memoria.field_names = ['Número bloque', 'Tamaño bloque', 'Número trabajo', 'Tiempo', 'Tamaño trabajo']
        for bloque in lista_memoria:
            tabla_memoria.add_row([bloque.numero, bloque.tamano, bloque.trabajo.numero, bloque.trabajo.tiempo, bloque.trabajo.tamano])

        print('Bloques de memoria:')
        print(tabla_memoria)

        tabla_trabajos = PrettyTable()
        tabla_trabajos.field_names = ['Número', 'Tiempo', 'Tamaño']
        for trabajo in lista_trabajos:
            tabla_trabajos.add_row([trabajo.numero, trabajo.tiempo, trabajo.tamano])

        print()
        print('Cola de trabajos:')
        print(tabla_trabajos)

        lista_mutex.release()

        names = [i.name for i in threading.enumerate()]
        if 'decrementar_tiempo' not in names:
            break

        time.sleep(1)


def decrementar_tiempo(lista_memoria: List[m.Bloque], lista_trabajos: List[m.Trabajo]):
    hay_trabajos = True
    while hay_trabajos:
        hay_trabajos = False
        lista_mutex.acquire()
        for bloque in lista_memoria:
            if bloque.ocupado:
                if bloque.trabajo.tiempo > 1:
                    bloque.trabajo.tiempo -= 1
                else:
                    bloque.modificar_trabajo(m.Trabajo(None, None, None))
                hay_trabajos = True
        lista_mutex.release()

        if not hay_trabajos and not lista_trabajos:
            break

        time.sleep(2)