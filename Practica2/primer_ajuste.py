import os
import time
from prettytable import PrettyTable
import threading


if os.name == "posix":
    var = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
    var = "cls"


def limpiar():
    os.system(var)


def imprimir_tabla(lista_memoria):
    while True:
        t = PrettyTable()
        t.field_names = ['Número bloque', 'Tamaño bloque', 'Número trabajo', 'Tiempo', 'Tamaño trabajo']
        for bloque in lista_memoria:
            if bloque.trabajo is not None:
                t.add_row([bloque.numero, bloque.tamano, bloque.trabajo.numero, bloque.trabajo.tiempo, bloque.trabajo.tamano])
            else:
                t.add_row([bloque.numero, bloque.tamano, 'Null', 'Null', 'Null'])
        limpiar()
        print(t)
        time.sleep(1)


def insertar_trabajos(lista_memoria, lista_trabajos: list):
    while lista_trabajos:
        for trabajo in lista_trabajos:
            #asignado = False
            for bloque in lista_memoria:
                if bloque.trabajo is None and bloque.tamano >= trabajo.tamano:
                    bloque.trabajo = trabajo
                    break
                #     lista_trabajos.remove(trabajo)
                #     asignado = True
                # elif bloque.trabajo.tiempo == 0:
                #     bloque.trabajo = None
                # else:
                #     bloque.trabajo.tiempo -= 1

            time.sleep(1)


def primer_ajuste(lista_memoria, lista_trabajos):
    d1 = threading.Thread(name='insertar_trabajos', target=insertar_trabajos, args=[lista_memoria, lista_trabajos], daemon=True)
    d2 = threading.Thread(name='imprimir_tabla', target=imprimir_tabla, args=[lista_memoria], daemon=True)
    d1.start()
    d2.start()
