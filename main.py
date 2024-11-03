from turing_machine import TuringMachine
import random
import json
from prettytable import PrettyTable
import os

def limpiar_pantalla():
    input('\nPresione Enter')
    os.system('cls')  # Comando para Windows
    

class ExtendedTuringMachine(TuringMachine):
    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=' '):
        super().__init__(transitions, start_state, accept_state, reject_state, blank_symbol)
        self.tape = []
        self.tape_preview = []

    def generar_cinta_aleatoria(self, largo=50):
        self.tape = [random.choice(['0', '1', '^']) for _ in range(largo)]
        self.tape_preview = self.tape.copy()
        print(f"Cinta generada: {self.tape}")
        self.definir_transiciones_aleatorias()

    def cargar_cinta(self, archivo):
        try:
            with open(archivo, 'r') as file:
                self.tape = json.load(file)
            print(f"Cinta cargada: {self.tape}")
        except FileNotFoundError:
            print("El archivo no se encontró.")

    def guardar_cinta(self, archivo):
        with open(archivo, 'w') as file:
            json.dump(self.tape, file)
        print(f"Cinta guardada en {archivo}")

    def mostrar_cinta(self):
        print(f'cinta actual: {self.tape}')
        print(f'cinta inicial: {self.tape_preview}')

    def actualizar_cinta(self, config):
        # Actualizar la cinta a partir de la configuración actual
        # Almacena en la cinta el contenido del lado izquierdo invertido, el símbolo actual, y el lado derecho
        self.tape = config['left_hand_side'][::-1] + [config['symbol']] + config['right_hand_side']
        print(f"Cinta actualizada: {self.tape}")

    def operar_maquina(self, estado_inicial, estado_paro):
        print(f"Iniciando en estado: {estado_inicial}")
        estado_num = int(estado_inicial[1:])  # Extrae el número del estado inicial
        estado_paro_num = int(estado_paro[1:])  # Extrae el número del estado de paro

        # Asegurarse de que la cinta sea lo suficientemente larga
        if len(self.tape) <= estado_paro_num:
            self.tape.extend([' '] * (estado_paro_num - len(self.tape) + 1))

        head_position = estado_num  # Establecer la posición inicial del cabezal
        paso = 0
        current_state = estado_inicial

        while True:
            print(
                f"\nCinta: {self.tape}\nPaso {paso}: Estado actual: {current_state}, Posición de la cinta: {head_position}, Símbolo actual: {self.tape[head_position]}")

            # Comprobar si hay un blanco en la celda actual
            if self.tape[head_position] == '^':
                print(f"Se encontró un blanco en el paso {paso}. No se puede continuar.")
                break

            # Preguntar al usuario si desea cambiar el símbolo actual
            cambiar = input(
                f"El símbolo actual es '{self.tape[head_position]}'. ¿Deseas cambiarlo? (s/n): ").strip().lower()
            if cambiar == 's':
                # Obtener el nuevo símbolo y el movimiento de usuario
                nuevo_simbolo = input(f"Ingresa el nuevo símbolo para reemplazar '{self.tape[head_position]}': ")
                movimiento = input("Ingresa el movimiento (D = derecha, I = izquierda, N = ninguno): ").strip().upper()

                # Validar el movimiento
                if movimiento not in ['D', 'I', 'N']:
                    print("Movimiento no permitido. Solo se permite 'D', 'I' o 'N'.")
                    continue

                # Actualizar el símbolo en la cinta
                self.tape[head_position] = nuevo_simbolo
            else:
                # Mantener el símbolo actual si el usuario no desea cambiarlo
                movimiento = input("Ingresa el movimiento (D = derecha, I = izquierda, N = ninguno): ").strip().upper()

                # Validar el movimiento
                if movimiento not in ['D', 'I', 'N']:
                    print("Movimiento no permitido. Solo se permite 'D', 'I' o 'N'.")
                    continue

            # Realizar el movimiento en la cinta
            if movimiento == 'D':  # Mover a la derecha
                if head_position < estado_paro_num:
                    head_position += 1
                else:
                    print("No se puede mover a la derecha, fin del rango permitido.")
                    break
            elif movimiento == 'I':  # Mover a la izquierda
                if head_position > estado_num:
                    head_position -= 1
                else:
                    print("No se puede mover a la izquierda, inicio del rango permitido.")
                    break
            elif movimiento == 'N':  # No realizar movimiento
                pass

            # Actualizar el estado de manera automática
            estado_num += 1
            current_state = f'q{estado_num}'

            # Incrementar el contador de pasos
            paso += 1

            # Verificar si se alcanzó el estado de paro
            if estado_num > estado_paro_num:
                print(f"Se alcanzó el estado de paro: {estado_paro} en el paso {paso}")
                break

    def definir_transiciones_aleatorias(self, num_estados=50, simbolos=['0', '1', '^']):
        transiciones = {}
        for estado in range(num_estados):
            for simbolo in simbolos:
                nuevo_estado = f'q{random.randint(0, num_estados)}'
                nuevo_simbolo = random.choice(simbolos)
                movimiento = random.choice(['L', 'R'])
                transiciones[(f'q{estado}', simbolo)] = (nuevo_estado, nuevo_simbolo, movimiento)

        # Agregar un estado de aceptación
        transiciones[(f'q{num_estados}', '')] = ('qa', '', 'R')
        self.transitions = transiciones

        # Mostrar las transiciones en una tabla
        tabla_transiciones = PrettyTable()
        tabla_transiciones.field_names = ["Estado Actual", "Símbolo Leído", "Nuevo Estado", "Símbolo Escrito",
                                          "Movimiento"]

        for (estado_actual, simbolo), (nuevo_estado, nuevo_simbolo, movimiento) in self.transitions.items():
            tabla_transiciones.add_row([estado_actual, simbolo, nuevo_estado, nuevo_simbolo, movimiento])

        print("Transiciones aleatorias definidas:")
        print(tabla_transiciones)

def mostrar_integrantes():
    table = PrettyTable()
    print('\n\n\t\t\tIntegrantes')    
    table.field_names = ['Nombre', 'Carne']    
    table.add_row(["VICTOR MANUEL MONJE OXLAJ", "5090-22-1172"])
    table.add_row(["ELMER DANIEL PÉREZ AVILA", "5090-22-3700"])
    table.add_row(["RAMIRO JOSÉ INTERIANO ORANTES", "5090-22-2434"])
    table.add_row(["DAVID ANTONIO MÉNDEZ ESTRADA", "5090-22-3128"])
    print(table)


def menu():
    maquina = ExtendedTuringMachine({})
    
    while True:
        mostrar_integrantes()
        print("\n--- Menú de Máquina de Turing ---")
        print("1. Generar cinta aleatoria")
        print("2. Cargar cinta desde archivo")
        print("3. Operar la máquina")
        print("4. Mostrar la cinta actual")
        print("5. Guardar cinta en archivo")
        print("6. Salir")

        opcion = input("Selecciona una opción (1-6): ")

        if opcion == '1':
            maquina.generar_cinta_aleatoria()

        elif opcion == '2':
            archivo = input("Ingrese el nombre del archivo para cargar la cinta: ")
            maquina.cargar_cinta(archivo)
        elif opcion == '3':
            estado_inicial = input("Ingrese el estado inicial (e.g., 'q0'): ")
            estado_paro = input("Ingrese el estado de paro (e.g., 'qa'): ")
            maquina.operar_maquina(estado_inicial, estado_paro)

        elif opcion == '4':
            maquina.mostrar_cinta()

        elif opcion == '5':
            archivo = input("Ingrese el nombre del archivo para guardar la cinta: ")
            maquina.guardar_cinta(archivo)

        elif opcion == '6':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")
        limpiar_pantalla()


if __name__ == "__main__":
    menu()
