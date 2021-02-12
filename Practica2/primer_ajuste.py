import time
import threading
import memoria as m
from typing import List
import memoria_global as mg


def insertar_trabajos(lista_memoria: List[m.Bloque], lista_trabajos: List[m.Trabajo]):
    while lista_trabajos:
        mg.lista_mutex.acquire()
        trabajo = lista_trabajos[0]

        for bloque in lista_memoria:
            if not bloque.ocupado and bloque.tamano >= trabajo.tamano:
                bloque.modificar_trabajo(trabajo)
                lista_trabajos.pop(0)
                break

        mg.lista_mutex.release()

        time.sleep(1)


def primer_ajuste(lista_memoria, lista_trabajos):
    d1 = threading.Thread(name='insertar_trabajos', target=insertar_trabajos, args=[lista_memoria, lista_trabajos], daemon=True)
    d2 = threading.Thread(name='imprimir_tabla', target=mg.imprimir_tabla, args=[lista_memoria], daemon=True)
    d3 = threading.Thread(name='decrementar_tiempo', target=mg.decrementar_tiempo, args=[lista_memoria, lista_trabajos], daemon=True)
    d1.start()
    d2.start()
    d3.start()
    d2.join()
