from turing_machine import TuringMachine
import random
import json
from prettytable import PrettyTable
import os
from colorama import Fore, Style, init

init()

def limpiar_pantalla():
    input('\nPresione Enter')
    os.system('cls')  # Comando para Windows
    

class ExtendedTuringMachine(TuringMachine):
    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=' '):
        super().__init__(transitions, start_state, accept_state, reject_state, blank_symbol)
        self.tape = []
        self.tape_preview = []
        self.modified_positions = []  # Almacena las posiciones modificadas

    def generar_cinta_aleatoria(self, largo=50):
        self.tape = [random.choice(['0', '1', '^']) for _ in range(largo)]
        self.tape_preview = self.tape.copy()
        print(f"Cinta generada: {self.tape}")

    def cargar_cinta(self, archivo):
        try:
            with open(archivo, 'r') as file:
                self.tape = json.load(file)
                self.tape_preview = self.tape.copy()  # Actualizar la cinta previa
                self.modified_positions = []  # Limpiar posiciones modificadas
            print(f"Cinta cargada: {self.tape}")
        except FileNotFoundError:
            print("El archivo no se encontró.")

    def guardar_cinta(self, archivo):
        with open(archivo, 'w') as file:
            json.dump(self.tape, file)
        print(f"Cinta guardada en {archivo}")

    def color_cinta(self, cinta):
        return ''.join(
            Fore.GREEN + simbolo + Style.RESET_ALL if simbolo == '0' else
            Fore.RED + simbolo + Style.RESET_ALL if simbolo == '1' else
            simbolo
            for simbolo in cinta
        )
        
    def mostrar_cinta(self):
        # Imprimir las posiciones modificadas
        modificados = ['*' if i in self.modified_positions else ' ' for i in range(len(self.tape))]
        print("Posiciones modificadas:\n" + ''.join(modificados))
        
        # Imprimir la cinta con colores
        
        print(f'{self.color_cinta(self.tape)}\n\n')
        print(f'Cinta inicial:\n{self.color_cinta(self.tape_preview)}\n\n')


    def actualizar_cinta(self, config):
        self.tape = config['left_hand_side'][::-1] + [config['symbol']] + config['right_hand_side']
        print(f"Cinta actualizada: {self.tape}")

    def operar_maquina(self, estado_inicial, estado_paro):
        print(f"Iniciando en estado: {estado_inicial}")
        estado_num = int(estado_inicial[1:])  # Extrae el número del estado inicial
        estado_paro_num = int(estado_paro[1:])  # Extrae el número del estado de paro

        if len(self.tape) <= estado_paro_num:
            self.tape.extend([' '] * (estado_paro_num - len(self.tape) + 1))

        head_position = estado_num  # Establecer la posición inicial del cabezal
        paso = 0
        current_state = estado_inicial

        while True:
            print(
                f"\nCinta: {self.color_cinta(self.tape)}\nPaso {paso}, Posición de la cinta: {head_position}, Símbolo actual: {self.tape[head_position]}")

            if self.tape[head_position] == '^':
                print(f"Se encontró un blanco en el paso {paso}. No se puede continuar.")
                break

            cambiar = input(
                f"El símbolo actual es '{self.tape[head_position]}'. ¿Deseas cambiarlo? (s/n): ").strip().lower()
            if cambiar == 's':
                nuevo_simbolo = input(f"Ingresa el nuevo símbolo para reemplazar '{self.tape[head_position]}': ")
                movimiento = input("Ingresa el movimiento (D = derecha, I = izquierda, N = ninguno): ").strip().upper()

                if movimiento not in ['D', 'I', 'N']:
                    print("Movimiento no permitido. Solo se permite 'D', 'I' o 'N'.")
                    continue

                self.tape[head_position] = nuevo_simbolo
                if head_position not in self.modified_positions:
                    self.modified_positions.append(head_position)
            else:
                movimiento = input("Ingresa el movimiento (D = derecha, I = izquierda, N = ninguno): ").strip().upper()

                if movimiento not in ['D', 'I', 'N']:
                    print("Movimiento no permitido. Solo se permite 'D', 'I' o 'N'.")
                    continue

            if movimiento == 'D':  # Mover a la derecha
                if head_position < estado_paro_num:
                    head_position += 1
                else:
                    print("No se puede mover a la derecha, fin del rango permitido.")
                    break
            elif movimiento == 'I':  # Mover a la izquierda
                head_position -= 1
            elif movimiento == 'N':  # No realizar movimiento
                pass

            estado_num += 1
            current_state = f'q{estado_num}'
            paso += 1

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

        transiciones[(f'q{num_estados}', '')] = ('qa', '', 'R')
        self.transitions = transiciones

        tabla_transiciones = PrettyTable()
        tabla_transiciones.field_names = ["Estado Actual", "Símbolo Leído", "Nuevo Estado", "Símbolo Escrito",
                                          "Movimiento"]

        for (estado_actual, simbolo), (nuevo_estado, nuevo_simbolo, movimiento) in self.transitions.items():
            tabla_transiciones.add_row([estado_actual, simbolo, nuevo_estado, nuevo_simbolo, movimiento])

        print("Transiciones aleatorias definidas:")
        print(tabla_transiciones)



def menu():
    maquina = ExtendedTuringMachine({})
    
    while True:
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
            maquina.definir_transiciones_aleatorias()  # Define transiciones automáticamente

        elif opcion == '4':
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
