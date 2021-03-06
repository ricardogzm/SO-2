import time
import memoria as m
import primer_ajuste as pa
import mejor_ajuste as ma
import memoria_global as mg


def menu():
    print("Ingrese una opción:")
    print("1. Primer ajuste")
    print("2. Mejor ajuste")
    print("3. Leer archivo de memoria")
    print("4. Leer archivo de trabajos")
    print("0. Salir")
    return int(input("> "))


def leer_memoria_txt(nombre_archivo: str):
    lista = []
    with open(nombre_archivo, "r") as f:
        content = f.readlines()
        for line in content:
            numero, tamano = line.split()
            lista.append(m.Bloque(int(numero), int(tamano)))

    return lista


def leer_trabajo_txt(nombre_archivo: str):
    lista = []
    with open(nombre_archivo, "r") as f:
        content = f.readlines()
        for line in content:
            numero, tiempo, tamano = line.split()
            lista.append(m.Trabajo(int(numero), int(tiempo), int(tamano)))

    return lista


if __name__ == '__main__':
    lista_memoria = []
    lista_trabajos = []
    while True:
        mg.limpiar()
        respuesta = menu()

        if respuesta == 0:
            break
        elif respuesta == 1:
            pa.primer_ajuste(lista_memoria, lista_trabajos)
        elif respuesta == 2:
            ma.mejor_ajuste(lista_memoria, lista_trabajos)
        elif respuesta == 3:
            # lista_memoria = leer_memoria_txt(input("Ingrese nombre del archivo: "))
            lista_memoria = leer_memoria_txt('lista_memoria.txt')
            print("\nArchivo leído con éxito.")
            time.sleep(1)

        elif respuesta == 4:
            # lista_trabajos = leer_trabajo_txt(input("Ingrese nombre del archivo: "))
            lista_trabajos = leer_trabajo_txt('lista_trabajos.txt')
            print("\nArchivo leído con éxito.")
            time.sleep(1)
        else:
            print("Opción inválida.")
