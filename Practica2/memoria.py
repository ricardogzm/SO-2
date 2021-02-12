class Trabajo:
    def __init__(self, numero: int, tiempo: int, tamano: int):
        self.numero = numero
        self.tiempo = tiempo
        self.tamano = tamano


class Bloque:
    def __init__(self, numero: int, tamano: int):
        self.numero = numero
        self.tamano = tamano
        self.trabajo = Trabajo(None, None, None)
        self.ocupado = False

    def modificar_trabajo(self, trabajo: Trabajo):
        self.ocupado = not self.ocupado
        self.trabajo = trabajo

