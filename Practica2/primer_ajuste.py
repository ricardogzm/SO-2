import os
import time
from prettytable import PrettyTable
import threading
import memoria as m
from typing import List


if os.name == "posix":
    var = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
    var = "cls"

# Definición de semáforos
# num_trabajos = threading.Semaphore(0)
lista_mutex = threading.Lock()


def limpiar():
    os.system(var)


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

    # t = PrettyTable()
    # t.field_names = ['Número bloque', 'Tamaño bloque', 'Número trabajo', 'Tiempo', 'Tamaño trabajo']
    # for bloque in lista_memoria:
    #     t.add_row([bloque.numero, bloque.tamano, bloque.trabajo.numero, bloque.trabajo.tiempo, bloque.trabajo.tamano])
    #
    # while True:
    #     limpiar()
    #     print(t)
    #     time.sleep(1)


def insertar_trabajos(lista_memoria: List[m.Bloque], lista_trabajos: List[m.Trabajo]):
    # while lista_trabajos:
    #     for trabajo in lista_trabajos:
    #         # asignado = False
    #         for bloque in lista_memoria:
    #             if bloque.trabajo is None and bloque.tamano >= trabajo.tamano:
    #                 bloque.trabajo = trabajo
    #                 break
    #             #     lista_trabajos.remove(trabajo)
    #             #     asignado = True
    #             # elif bloque.trabajo.tiempo == 0:
    #             #     bloque.trabajo = None
    #             # else:
    #             #     bloque.trabajo.tiempo -= 1
    #
    #         time.sleep(1)

    i = -1
    while lista_trabajos:
        lista_mutex.acquire()
        i = (i+1) % len(lista_trabajos)
        trabajo = lista_trabajos[i]
        for bloque in lista_memoria:
            if not bloque.ocupado and bloque.tamano >= trabajo.tamano:
                bloque.modificar_trabajo(trabajo)
                lista_trabajos.pop(i)
                i -= 1
                # num_trabajos.release()
                break
        lista_mutex.release()

        time.sleep(1)


def decrementar_tiempo(lista_memoria: List[m.Bloque], lista_trabajos: List[m.Trabajo]):
    hay_trabajos = True
    while hay_trabajos:
        hay_trabajos = False
        # num_trabajos.acquire()
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


def primer_ajuste(lista_memoria, lista_trabajos):
    d1 = threading.Thread(name='insertar_trabajos', target=insertar_trabajos, args=[lista_memoria, lista_trabajos], daemon=True)
    d2 = threading.Thread(name='imprimir_tabla', target=imprimir_tabla, args=[lista_memoria], daemon=True)
    d3 = threading.Thread(name='decrementar_tiempo', target=decrementar_tiempo, args=[lista_memoria, lista_trabajos], daemon=True)
    d1.start()
    d2.start()
    d3.start()
    d2.join()
