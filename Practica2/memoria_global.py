
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


def imprimir_tabla(lista_memoria: List[m.Bloque]):
    while True:
        t = PrettyTable()
        t.field_names = ['Número bloque', 'Tamaño bloque', 'Número trabajo', 'Tiempo', 'Tamaño trabajo']
        for bloque in lista_memoria:
            t.add_row([bloque.numero, bloque.tamano, bloque.trabajo.numero, bloque.trabajo.tiempo, bloque.trabajo.tamano])
        limpiar()
        print(t)
        time.sleep(1)

        names = [i.name for i in threading.enumerate()]
        if 'decrementar_tiempo' not in names:
            break


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